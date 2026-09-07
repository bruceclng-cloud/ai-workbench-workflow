#!/usr/bin/env python3
"""Bootstrap installer for the legacy AI Workbench Workflow v0.2 distribution.

The retained v0.2.0 package is a historical reproducibility artifact. Current
workflow authority ends at Feather, while that package may contain superseded
Task/Tasks hierarchy wording. Installing it into a live project therefore
requires an explicit legacy override until a corrected package is published.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import io
import lzma
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARTS = sorted(HERE.glob("workbench-workflow-v0.2.0.part*"))
PACKAGE_SHA256 = "e6af624ec5296b7a18e118632f663cb5c81be8d365ebe09da80ba88a084efa2e"


def extract_source(dest: Path) -> None:
    if not PARTS:
        raise SystemExit("Missing workbench-workflow-v0.2.0.part* files")
    encoded = "".join(p.read_text(encoding="ascii").strip() for p in PARTS)
    try:
        compressed = base64.b64decode(encoded, validate=True)
        actual = hashlib.sha256(compressed).hexdigest()
        if actual != PACKAGE_SHA256:
            raise ValueError(
                f"package SHA256 mismatch: expected {PACKAGE_SHA256}, got {actual}"
            )
        tar_bytes = lzma.decompress(compressed)
    except Exception as exc:
        raise SystemExit(f"Package integrity/decode failure: {exc}") from exc

    dest.mkdir(parents=True, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(tar_bytes), mode="r:") as tf:
        root = dest.resolve()
        for member in tf.getmembers():
            target = (dest / member.name).resolve()
            if root not in target.parents and target != root:
                raise SystemExit(f"Unsafe archive path: {member.name}")
        tf.extractall(dest)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inspect or explicitly install the legacy AI Workbench Workflow v0.2 package"
    )
    parser.add_argument(
        "target", nargs="?", default=".", help="target repository (default: current directory)"
    )
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--extract-source", metavar="DIR", help="extract the historical v0.2.0 source without installing"
    )
    parser.add_argument(
        "--allow-legacy-v0-2",
        action="store_true",
        help=(
            "explicitly install the historical v0.2.0 package despite superseded "
            "Task/Tasks hierarchy wording; not recommended for new project authority"
        ),
    )
    args = parser.parse_args()

    if args.extract_source:
        dest = Path(args.extract_source).expanduser().resolve()
        extract_source(dest)
        print(f"Extracted historical v0.2.0 source to {dest}")
        print("Current workflow authority is North → Bird → Wing → Feather; see WORKFLOW.md.")
        return 0

    if not args.allow_legacy_v0_2:
        raise SystemExit(
            "Refusing to install the historical v0.2.0 package into a live project by default.\n"
            "Current authority is North → Bird → Wing → Feather, while the retained release "
            "may inject superseded Task/Tasks wording.\n"
            "Use --extract-source to inspect it, or --allow-legacy-v0-2 only when deliberately "
            "reproducing the old release. Publish/use a corrected package for current projects."
        )

    target = Path(args.target).expanduser().resolve()
    with tempfile.TemporaryDirectory(prefix="ai-workbench-workflow-") as td:
        source = Path(td)
        extract_source(source)
        cmd = [sys.executable, str(source / "install.py"), str(target)]
        if args.force:
            cmd.append("--force")
        if args.dry_run:
            cmd.append("--dry-run")
        return subprocess.call(cmd)


if __name__ == "__main__":
    raise SystemExit(main())
