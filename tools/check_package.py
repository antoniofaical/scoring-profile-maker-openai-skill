"""Check skill metadata, local links and bundled resource integrity."""

import hashlib
import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/scoring-profile-maker"


def check() -> list[str]:
    errors = []
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return ["Missing frontmatter"]
    frontmatter = yaml.safe_load(match[1])
    if frontmatter.get("name") != SKILL.name or not frontmatter.get("description"):
        errors.append("Invalid skill discovery metadata")
    metadata = yaml.safe_load((SKILL / "agents/openai.yaml").read_text(encoding="utf-8"))
    interface = metadata.get("interface", {})
    if not 25 <= len(interface.get("short_description", "")) <= 64:
        errors.append("Invalid short description length")
    if "$scoring-profile-maker" not in interface.get("default_prompt", ""):
        errors.append("Default prompt must name the skill")
    if metadata.get("policy", {}).get("allow_implicit_invocation") is False:
        errors.append("Implicit invocation should remain enabled")
    for document in SKILL.rglob("*.md"):
        body = document.read_text(encoding="utf-8")
        if "[TODO:" in body:
            errors.append(f"Unfinished scaffold: {document.relative_to(SKILL)}")
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", body):
            if "://" in target or target.startswith("#"):
                continue
            path = (document.parent / target.split("#")[0]).resolve()
            if not path.is_relative_to(SKILL.resolve()) or not path.exists():
                errors.append(f"Broken or external local link: {target}")
    manifest = json.loads((SKILL / "references/upstream.json").read_text(encoding="utf-8"))
    for entry in manifest["resources"]:
        path = SKILL / entry["target"]
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != entry["bundled_sha256"]:
            errors.append(f"Bundled contract integrity mismatch: {entry['target']}")
    return errors


if __name__ == "__main__":
    failures = check()
    if failures:
        raise SystemExit("\n".join(failures))
    print("Package metadata, links and provenance hashes valid")
