"""Snapshot authorized read-only classifier resources into this skill."""

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "scoring-profile-maker"
REPOSITORY = "https://github.com/antoniofaical/startup-theme-adherence-classifier-jev"
RESOURCES = {
    "profiles/profile.schema.json": "references/profile.schema.json",
    "profiles/profile.template.json": "assets/profile.template.json",
    "profiles/profile_request.template.json": "assets/profile_request.template.json",
    "profiles/digital_twin.json": "references/examples/digital_twin.json",
    "profiles/gsd_patient_journey_mapping.json": "references/examples/gsd_patient_journey_mapping.json",
    "src/startup_adherence/domain/profile.py": "scripts/_profile_contract.py",
}


def adapt_runtime(source: str) -> str:
    old = 'files("startup_adherence.profiles")\n        .joinpath("profile.schema.json")'
    new = '(Path(__file__).resolve().parents[1] / "references" / "profile.schema.json")'
    if source.count(old) != 1:
        raise ValueError("Upstream schema loader changed; review the adaptation")
    return source.replace("from importlib.resources import files\n", "").replace(old, new)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("classifier_root", type=Path)
    parser.add_argument("--date", required=True, help="Verification date, YYYY-MM-DD")
    args = parser.parse_args()
    checkout = args.classifier_root.resolve()
    commit = subprocess.check_output(
        ["git", "-C", str(checkout), "rev-parse", "HEAD"], text=True
    ).strip()
    entries = []
    for source_path, target_path in RESOURCES.items():
        content = subprocess.check_output(
            ["git", "-C", str(checkout), "show", f"{commit}:{source_path}"]
        )
        output = (
            adapt_runtime(content.decode("utf-8")).encode("utf-8")
            if source_path.endswith("/profile.py")
            else content
        )
        target = SKILL / target_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(output)
        entries.append({
            "source": source_path,
            "url": f"{REPOSITORY}/blob/{commit}/{source_path}",
            "target": target_path,
            "source_sha256": hashlib.sha256(content).hexdigest(),
            "bundled_sha256": hashlib.sha256(output).hexdigest(),
            "adaptation": "schema loader path only; removed unused files import"
            if output != content else None,
        })
    manifest = {
        "repository": REPOSITORY,
        "commit": commit,
        "verified_on": args.date,
        "profile_schema_version": 1,
        "resources": entries,
        "method_sources": [
            f"{REPOSITORY}/blob/{commit}/profiles/HOW_TO_CREATE_PROFILES.md",
            f"{REPOSITORY}/blob/{commit}/profiles/PROFILE_GENERATION_PROMPT.md",
            f"{REPOSITORY}/blob/{commit}/src/startup_adherence/domain/scoring.py",
            f"{REPOSITORY}/blob/{commit}/README.md",
        ],
    }
    (SKILL / "references" / "upstream.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Snapshotted {len(entries)} resources from {commit}")


if __name__ == "__main__":
    main()
