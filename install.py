#!/usr/bin/env python3
"""Bootstrap installer for AI Workbench Workflow v0.2 public distribution."""
from __future__ import annotations
import argparse, base64, hashlib, io, lzma, subprocess, sys, tarfile, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARTS = sorted(HERE.glob('workbench-workflow-v0.2.0.part*'))
PACKAGE_SHA256 = 'e6af624ec5296b7a18e118632f663cb5c81be8d365ebe09da80ba88a084efa2e'


def extract_source(dest: Path) -> None:
    if not PARTS:
        raise SystemExit('Missing workbench-workflow-v0.2.0.part* files')
    encoded = ''.join(p.read_text(encoding='ascii').strip() for p in PARTS)
    try:
        compressed = base64.b64decode(encoded, validate=True)
        actual = hashlib.sha256(compressed).hexdigest()
        if actual != PACKAGE_SHA256:
            raise ValueError(f'package SHA256 mismatch: expected {PACKAGE_SHA256}, got {actual}')
        tar_bytes = lzma.decompress(compressed)
    except Exception as exc:
        raise SystemExit(f'Package integrity/decode failure: {exc}') from exc
    dest.mkdir(parents=True, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(tar_bytes), mode='r:') as tf:
        root = dest.resolve()
        for member in tf.getmembers():
            target = (dest / member.name).resolve()
            if root not in target.parents and target != root:
                raise SystemExit(f'Unsafe archive path: {member.name}')
        tf.extractall(dest)


def main() -> int:
    p = argparse.ArgumentParser(description='Install AI Workbench Workflow into a project')
    p.add_argument('target', nargs='?', default='.', help='target repository (default: current directory)')
    p.add_argument('--force', action='store_true')
    p.add_argument('--dry-run', action='store_true')
    p.add_argument('--extract-source', metavar='DIR', help='extract complete source instead of installing')
    args = p.parse_args()

    if args.extract_source:
        dest = Path(args.extract_source).expanduser().resolve()
        extract_source(dest)
        print(f'Extracted complete v0.2.0 source to {dest}')
        return 0

    target = Path(args.target).expanduser().resolve()
    with tempfile.TemporaryDirectory(prefix='ai-workbench-workflow-') as td:
        source = Path(td)
        extract_source(source)
        cmd = [sys.executable, str(source / 'install.py'), str(target)]
        if args.force:
            cmd.append('--force')
        if args.dry_run:
            cmd.append('--dry-run')
        return subprocess.call(cmd)


if __name__ == '__main__':
    raise SystemExit(main())
