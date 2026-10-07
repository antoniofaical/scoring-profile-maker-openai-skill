"""Meaningful contract, answer-identity, CLI and distribution regressions."""

import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/scoring-profile-maker"
sys.path.insert(0, str(SKILL / "scripts"))
sys.path.insert(0, str(ROOT / "tools"))
sys.dont_write_bytecode = True
from validate_profile import compare_profiles, make_report, read_profile
from _profile_contract import validate_profile, profile_sha256, question_set_sha256
from check_package import check
from package_skill import package


def example():
    return json.loads((SKILL / "references/examples/digital_twin.json").read_text(encoding="utf-8"))


def invalid_profiles():
    cases = []
    def mutate(name, fn):
        profile = example()
        fn(profile)
        cases.append((name, profile))
    mutate("unknown field", lambda p: p.update(status="approved"))
    mutate("wrong schema", lambda p: p.update(profile_schema_version=2))
    mutate("unsafe id", lambda p: p.update(id="../profile"))
    mutate("blank instruction", lambda p: p.update(instruction="  "))
    mutate("empty criteria", lambda p: p.update(criteria=[]))
    mutate("duplicate ids", lambda p: p["criteria"].append(copy.deepcopy(p["criteria"][0])))
    mutate("no core", lambda p: p.update(criteria=[{"id": "context", "role": "auxiliary", "instructions": "Is the label explicit?"}]))
    mutate("weight zero", lambda p: p["criteria"][0].update(weight=0))
    mutate("weight boolean", lambda p: p["criteria"][0].update(weight=True))
    mutate("weight infinity", lambda p: p["criteria"][0].update(weight=float("inf")))
    mutate("blank question", lambda p: p["criteria"][0].update(instructions=" "))
    mutate("threshold on core", lambda p: p["criteria"][0].update(threshold=0.7))
    mutate("weight on auxiliary", lambda p: p["criteria"][-1].update(weight=1))
    mutate("threshold > 1", lambda p: p["criteria"][-1].update(threshold=1.1))
    mutate("threshold boolean", lambda p: p["criteria"][-1].update(threshold=False))
    mutate("evidence weight zero", lambda p: p["evidence_aggregation"].update(top_weights=[0]))
    mutate("evidence weight infinite", lambda p: p["evidence_aggregation"].update(top_weights=[float("inf")]))
    mutate("invented OR aggregate", lambda p: p.update(score_aggregation={"method": "maximum"}))
    mutate("empty bottleneck", lambda p: p["score_aggregation"].update(geometric_weight=0, bottleneck_weight=0))
    mutate("negative bottleneck", lambda p: p["score_aggregation"].update(geometric_weight=-1))
    return cases


class ContractTests(unittest.TestCase):
    def test_bundled_profiles_and_template_valid(self):
        for path in [*SKILL.glob("references/examples/*.json"), SKILL / "assets/profile.template.json"]:
            with self.subTest(path=path.name):
                profile = read_profile(path)
                self.assertGreaterEqual(sum(c["role"] == "core" for c in profile["criteria"]), 1)

    def test_all_supported_aggregations(self):
        for evidence in ("top_weighted", "mean", "maximum"):
            for score in ("weighted_mean", "weighted_geometric", "minimum", "weighted_geometric_bottleneck"):
                with self.subTest(evidence=evidence, score=score):
                    profile = example()
                    profile["evidence_aggregation"] = {"method": evidence}
                    profile["score_aggregation"] = {"method": score}
                    validate_profile(profile)

    def test_invalid_contracts_rejected(self):
        for name, profile in invalid_profiles():
            with self.subTest(case=name):
                with self.assertRaises(Exception):
                    validate_profile(profile)

    def test_strict_json_rejects_ambiguous_inputs(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.json"
            for content in ('{"id":"first","id":"second"}', '{"weight":NaN}', '{"weight":1e999}', '[]'):
                with self.subTest(content=content):
                    path.write_text(content, encoding="utf-8")
                    with self.assertRaises((ValueError, TypeError)):
                        read_profile(path)

    def test_scoring_changes_preserve_answer_identity(self):
        baseline = example()
        for change in ("weight", "threshold", "role", "evidence", "score", "reorder"):
            profile = copy.deepcopy(baseline)
            if change == "weight":
                profile["criteria"][0]["weight"] = 2
            elif change == "threshold":
                profile["criteria"][-1]["threshold"] = 0.8
            elif change == "role":
                profile["criteria"][-1]["role"] = "core"
            elif change == "evidence":
                profile["evidence_aggregation"] = {"method": "maximum"}
            elif change == "score":
                profile["score_aggregation"] = {"method": "minimum"}
            else:
                profile["criteria"].reverse()
            with self.subTest(change=change):
                validate_profile(profile)
                self.assertEqual(question_set_sha256(profile), question_set_sha256(baseline))
                self.assertNotEqual(profile_sha256(profile), profile_sha256(baseline))
                self.assertTrue(compare_profiles(profile, baseline)["saved_answers_compatible_for_text_replay"])

    def test_question_changes_require_new_answers(self):
        baseline = example()
        for change in ("instruction", "question", "id", "add", "remove"):
            profile = copy.deepcopy(baseline)
            if change == "instruction":
                profile["instruction"] += " Do not infer missing capabilities."
            elif change == "question":
                profile["criteria"][0]["instructions"] += " Explicitly?"
            elif change == "id":
                profile["criteria"][0]["id"] = "renamed_dimension"
            elif change == "add":
                profile["criteria"].append({"id": "new_dimension", "role": "auxiliary", "instructions": "Is a new signal explicit?"})
            else:
                profile["criteria"].pop()
            with self.subTest(change=change):
                report = compare_profiles(profile, baseline)
                self.assertFalse(report["saved_answers_compatible_for_text_replay"])
                self.assertEqual(report["suggested_version_change"], "major")

    def test_identity_boundaries_and_version_warnings(self):
        baseline = example()
        self.assertEqual(compare_profiles(baseline, baseline)["suggested_version_change"], "none")
        profile = copy.deepcopy(baseline)
        profile["description"] += " Revised documentation."
        self.assertEqual(compare_profiles(profile, baseline)["suggested_version_change"], "patch")
        self.assertTrue(compare_profiles(profile, baseline)["warnings"])
        profile["id"] = "different_identity"
        report = compare_profiles(profile, baseline)
        self.assertTrue(report["saved_answers_compatible_for_text_replay"])
        self.assertFalse(report["saved_site_run_compatible_for_score_lookup"])

    def test_cli_reports_real_success_and_failure(self):
        valid = subprocess.run(
            [sys.executable, str(SKILL / "scripts/validate_profile.py"), str(SKILL / "references/examples/digital_twin.json")],
            capture_output=True, text=True, encoding="utf-8",
        )
        self.assertEqual(valid.returncode, 0, valid.stderr)
        self.assertTrue(json.loads(valid.stdout)["valid"])
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.json"
            path.write_text('{"generation_error":["target missing"]}', encoding="utf-8")
            failed = subprocess.run([sys.executable, str(SKILL / "scripts/validate_profile.py"), str(path)], capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(failed.returncode, 1)
            self.assertFalse(json.loads(failed.stderr)["valid"])

    def test_cli_diagnostics_are_utf8_under_legacy_parent_encoding(self):
        profile = example()
        profile["criteria"][0]["weight"] = "peso inválido 🧭"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.json"
            path.write_text(json.dumps(profile, ensure_ascii=False), encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, str(SKILL / "scripts/validate_profile.py"), str(path)],
                env={**os.environ, "PYTHONIOENCODING": "cp1252"}, capture_output=True,
            )
            self.assertEqual(completed.returncode, 1)
            report = json.loads(completed.stderr.decode("utf-8"))
            self.assertFalse(report["valid"])
            self.assertIn("🧭", report["error"])


class DistributionTests(unittest.TestCase):
    def test_package_metadata_links_and_hashes(self):
        self.assertEqual(check(), [])

    def test_zip_is_deterministic_and_self_contained(self):
        with tempfile.TemporaryDirectory() as directory:
            first = package(Path(directory) / "one.zip")
            second = package(Path(directory) / "two.zip")
            self.assertEqual(first.read_bytes(), second.read_bytes())
            with ZipFile(first) as archive:
                names = archive.namelist()
                self.assertIn("scoring-profile-maker/SKILL.md", names)
                self.assertFalse(any("__pycache__" in name or ".venv" in name or "auditoria" in name for name in names))
                archive.extractall(Path(directory) / "extracted")
            relocated = Path(directory) / "extracted/scoring-profile-maker"
            completed = subprocess.run(
                [sys.executable, str(relocated / "scripts/validate_profile.py"), str(relocated / "references/examples/digital_twin.json")],
                capture_output=True, text=True, encoding="utf-8", cwd=directory,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertTrue(json.loads(completed.stdout)["valid"])


@unittest.skipUnless(os.environ.get("CLASSIFIER_ROOT"), "Optional real classifier checkout unavailable")
class UpstreamParityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.checkout = Path(os.environ["CLASSIFIER_ROOT"]).resolve()
        sys.path.insert(0, str(cls.checkout / "src"))
        from startup_adherence.domain import profile as runtime
        cls.runtime = runtime

    def test_real_runtime_validation_and_hashes(self):
        for path in SKILL.glob("references/examples/*.json"):
            report = make_report(path, classifier_root=self.checkout)
            self.assertTrue(report["classifier_runtime"]["valid"])
            self.assertTrue(report["classifier_runtime"]["schema_matches_bundled"])

    def test_invalid_corpus_matches_authoritative_runtime(self):
        for name, profile in invalid_profiles():
            with self.subTest(case=name):
                with self.assertRaises(Exception):
                    self.runtime.validate_profile(profile)

    def test_compatible_revisions_have_same_upstream_hash(self):
        baseline = example()
        revised = copy.deepcopy(baseline)
        revised["version"] = "1.1.0"
        revised["criteria"][2]["weight"] = 2.0
        self.assertEqual(self.runtime.question_set_sha256(revised), question_set_sha256(revised))
        self.assertEqual(self.runtime.question_set_sha256(revised), self.runtime.question_set_sha256(baseline))


if __name__ == "__main__":
    unittest.main()
