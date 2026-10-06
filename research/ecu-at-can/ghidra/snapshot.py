#!/usr/bin/env python3
"""Archive a closed Ghidra project with a per-file SHA256 inventory."""
import gzip
import hashlib
import io
import json
from pathlib import Path
import tarfile


def snapshot():
    root = Path(__file__).resolve().parent
    live = root / "live"
    project = "nc-at-can"
    if list(live.glob("*.lock*")):
        raise SystemExit("Close Ghidra/headless before making a snapshot")
    gpr = live / f"{project}.gpr"
    rep = live / f"{project}.rep"
    if not gpr.is_file() or not rep.is_dir():
        raise SystemExit("Missing live project .gpr or .rep")
    paths = [gpr] + sorted(p for p in rep.rglob("*") if p.is_file())
    inventory = {}
    temporary = root / f"{project}.tar.gz.tmp"
    archive = root / f"{project}.tar.gz"
    with temporary.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as zipped:
            with tarfile.open(fileobj=zipped, mode="w") as tar:
                for path in paths:
                    if path.is_symlink():
                        raise SystemExit(f"Unexpected symlink: {path}")
                    data = path.read_bytes()
                    name = path.relative_to(live).as_posix()
                    inventory[name] = hashlib.sha256(data).hexdigest()
                    info = tarfile.TarInfo(name)
                    info.size = len(data)
                    info.mode = 0o600
                    tar.addfile(info, io.BytesIO(data))
    # Read every archived byte back before replacing the previous snapshot.
    with tarfile.open(temporary) as tar:
        actual = {m.name: hashlib.sha256(tar.extractfile(m).read()).hexdigest()
                  for m in tar.getmembers()}
    if actual != inventory:
        raise SystemExit("Archive read-back failed; previous snapshot retained")
    temporary.replace(archive)
    manifest = {"archive": archive.name,
                "sha256": hashlib.sha256(archive.read_bytes()).hexdigest(),
                "files": inventory}
    (root / "snapshot.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Saved and verified {archive.name}: {len(inventory)} files, "
          f"{archive.stat().st_size:,} bytes")


if __name__ == "__main__":
    snapshot()
