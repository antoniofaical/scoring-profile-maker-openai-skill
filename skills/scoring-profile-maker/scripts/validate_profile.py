"""Validate a profile offline and report the saved-answer compatibility boundary."""

from __future__ import annotations

import argparse
import json
import math
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

try:
    from _profile_contract import (
        profile_sha256,
        question_set_sha256,
        validate_profile,
    )
    from jsonschema.exceptions import ValidationError
except ModuleNotFoundError as exc:
    if exc.name != "jsonschema":
        raise
    print("Missing jsonschema. Install: python -m pip install 'jsonschema>=4.21,<5'", file=sys.stderr)
    raise SystemExit(1) from exc

SKILL = Path(__file__).resolve().parents[1]


def _unique_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_constant(value: str) -> None:
    raise ValueError(f"Non-finite JSON number: {value}")


def _check_finite(value: Any) -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("Non-finite JSON number")
    if isinstance(value, dict):
        for child in value.values():
            _check_finite(child)
    elif isinstance(value, list):
        for child in value:
            _check_finite(child)


def read_profile(path: Path) -> dict[str, Any]:
    profile = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=_unique_keys,
        parse_constant=_reject_constant,
    )
    _check_finite(profile)
    if not isinstance(profile, dict):
        raise TypeError("Profile must be a JSON object")
    validate_profile(profile)
    return profile


def compare_profiles(profile: dict[str, Any], baseline: dict[str, Any]) -> dict[str, Any]:
    old = {item["id"]: item for item in baseline["criteria"]}
    new = {item["id"]: item for item in profile["criteria"]}
    same_questions = question_set_sha256(profile) == question_set_sha256(baseline)
    same_id = profile["id"] == baseline["id"]
    scoring_changed = (
        profile["evidence_aggregation"] != baseline["evidence_aggregation"]
        or profile["score_aggregation"] != baseline["score_aggregation"]
        or any(
            {k: v for k, v in old[key].items() if k not in {"id", "instructions"}}
            != {k: v for k, v in new[key].items() if k not in {"id", "instructions"}}
            for key in old.keys() & new.keys()
        )
    )
    same_profile = profile_sha256(profile) == profile_sha256(baseline)
    bump = (
        "new_identity" if not same_id else
        "major" if not same_questions else
        "minor" if scoring_changed else
        "none" if same_profile else "patch"
    )
    warnings = []
    if not same_profile and same_id and profile["version"] == baseline["version"]:
        warnings.append("Profile content changed without a version change")
    return {
        "baseline": {"id": baseline["id"], "version": baseline["version"]},
        "same_profile_id": same_id,
        "same_question_set": same_questions,
        "saved_answers_compatible_for_text_replay": same_questions,
        "saved_site_run_compatible_for_score_lookup": same_id and same_questions,
        "shared_instruction_changed": profile["instruction"] != baseline["instruction"],
        "added_criterion_ids": sorted(new.keys() - old.keys()),
        "removed_criterion_ids": sorted(old.keys() - new.keys()),
        "changed_question_ids": sorted(
            key for key in old.keys() & new.keys()
            if old[key]["instructions"] != new[key]["instructions"]
        ),
        "suggested_version_change": bump,
        "warnings": warnings,
        "limits": "Compatibility requires saved records with matching hashes, a consistent model, all criteria, and a completed run where applicable; semantic review remains necessary.",
    }


def check_classifier(path: Path, classifier_root: Path) -> dict[str, Any]:
    root = classifier_root.resolve()
    module = root / "src/startup_adherence/domain/profile.py"
    schema = root / "src/startup_adherence/profiles/profile.schema.json"
    if not module.is_file() or not schema.is_file():
        raise ValueError("Classifier root must contain src/startup_adherence domain and profile schema")
    code = """
import json, sys
sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from startup_adherence.domain.profile import load_profile, profile_sha256, question_set_sha256
profile = load_profile(Path(sys.argv[2]))
print(json.dumps({'valid': True, 'profile_sha256': profile_sha256(profile),
                  'question_set_sha256': question_set_sha256(profile)}))
"""
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONIOENCODING": "utf-8"}
    completed = subprocess.run(
        [sys.executable, "-c", code, str(root / "src"), str(path.resolve())],
        cwd=root, env=env, capture_output=True, text=True, encoding="utf-8", timeout=30,
    )
    if completed.returncode:
        raise ValueError(f"Classifier runtime validation failed: {completed.stderr.strip()}")
    result = json.loads(completed.stdout)
    result["schema_matches_bundled"] = (
        json.loads(schema.read_text(encoding="utf-8"))
        == json.loads((SKILL / "references/profile.schema.json").read_text(encoding="utf-8"))
    )
    result["root"] = str(root)
    try:
        result["commit"] = subprocess.check_output(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            text=True, stderr=subprocess.DEVNULL, timeout=10,
        ).strip()
    except (OSError, subprocess.SubprocessError):
        result["commit"] = None
    result["revision_scope"] = "Working checkout runtime; commit does not assert a clean checkout"
    return result


def make_report(path: Path, baseline: Path | None = None, classifier_root: Path | None = None) -> dict[str, Any]:
    profile = read_profile(path)
    upstream = json.loads((SKILL / "references/upstream.json").read_text(encoding="utf-8"))
    report: dict[str, Any] = {
        "valid": True,
        "validation_scope": "Bundled JSON Schema plus runtime invariants; not semantic approval or empirical calibration",
        "profile": {"id": profile["id"], "version": profile["version"]},
        "profile_sha256": profile_sha256(profile),
        "question_set_sha256": question_set_sha256(profile),
        "core_count": sum(item["role"] == "core" for item in profile["criteria"]),
        "auxiliary_count": sum(item["role"] == "auxiliary" for item in profile["criteria"]),
        "bundled_classifier_commit": upstream["commit"],
    }
    if baseline is not None:
        report["comparison"] = compare_profiles(profile, read_profile(baseline))
    if classifier_root is not None:
        live = check_classifier(path, classifier_root)
        for key in ("profile_sha256", "question_set_sha256"):
            if live[key] != report[key]:
                raise ValueError(f"Classifier identity differs from bundled identity: {key}")
        if baseline is not None:
            original = read_profile(baseline)
            live_baseline = check_classifier(baseline, classifier_root)
            if live_baseline["question_set_sha256"] != question_set_sha256(original):
                raise ValueError("Classifier baseline question identity differs")
        report["classifier_runtime"] = live
    return report


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profile", type=Path)
    parser.add_argument("--baseline", type=Path)
    parser.add_argument("--classifier-root", type=Path)
    args = parser.parse_args()
    try:
        report = make_report(args.profile, args.baseline, args.classifier_root)
    except Exception as exc:
        failure: dict[str, Any] = {"valid": False, "error": str(exc)}
        if isinstance(exc, ValidationError):
            failure.update(error=exc.message, path=list(exc.absolute_path))
        print(json.dumps(failure, ensure_ascii=False), file=sys.stderr)
        return 1
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
