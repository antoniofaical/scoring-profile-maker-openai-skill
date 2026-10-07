"""Build a deterministic ZIP containing only the distributable skill."""

import hashlib
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/scoring-profile-maker"
VERSION = "0.1.0"


def package(destination: Path | None = None) -> Path:
    destination = destination or ROOT / f"dist/scoring-profile-maker-{VERSION}.zip"
    destination.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(destination, "w", compression=ZIP_DEFLATED) as archive:
        for path in sorted(SKILL.rglob("*")):
            if not path.is_file() or "__pycache__" in path.parts or path.suffix == ".pyc":
                continue
            info = ZipInfo(f"{SKILL.name}/{path.relative_to(SKILL).as_posix()}", date_time=(2026, 10, 7, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            content = path.read_bytes()
            if path.suffix in {".md", ".json", ".py", ".yaml", ".yml", ".txt"}:
                content = content.replace(b"\r\n", b"\n")
            archive.writestr(info, content)
    print(json.dumps({"path": str(destination), "sha256": hashlib.sha256(destination.read_bytes()).hexdigest()}))
    return destination


if __name__ == "__main__":
    package()
