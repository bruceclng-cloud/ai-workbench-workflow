#!/usr/bin/env python3
"""Bootstrap installer for AI Workbench Workflow public distribution.

This repository ships the canonical source tree in workbench-workflow.bundle.json so
one download is enough. By default this extracts the bundle to a temporary directory
and runs the canonical source install.py against the target project.
"""
from __future__ import annotations
import argparse, base64, hashlib, json, os, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUNDLE_PARTS = sorted(HERE.glob('workbench-workflow.bundle.part*'))


def extract_bundle(dest: Path) -> None:
    if not BUNDLE_PARTS:
        raise SystemExit('Missing bundle parts')
    data = json.loads(''.join(p.read_text(encoding='utf-8') for p in BUNDLE_PARTS))
    if data.get('format') != 'ai-workbench-workflow-bundle-v1':
        raise SystemExit('Unsupported bundle format')
    for rel, rec in data['files'].items():
        raw = base64.b64decode(rec['content_b64'])
        digest = hashlib.sha256(raw).hexdigest()
        if digest != rec['sha256']:
            raise SystemExit(f'Integrity check failed for {rel}')
        path = dest / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
        if rec.get('mode') == '100755':
            path.chmod(path.stat().st_mode | 0o111)


def main() -> int:
    p = argparse.ArgumentParser(description='Install AI Workbench Workflow into a project')
    p.add_argument('target', nargs='?', default='.', help='target repository (default: current directory)')
    p.add_argument('--force', action='store_true', help='allow canonical installer to replace conflicting workflow files')
    p.add_argument('--dry-run', action='store_true')
    p.add_argument('--extract-source', metavar='DIR', help='extract the complete source package instead of installing')
    args = p.parse_args()

    if not BUNDLE_PARTS:
        print('ERROR: missing workbench-workflow.bundle.part* files', file=sys.stderr)
        return 2

    if args.extract_source:
        dest = Path(args.extract_source).expanduser().resolve()
        dest.mkdir(parents=True, exist_ok=True)
        extract_bundle(dest)
        print(f'Extracted complete source to {dest}')
        return 0

    target = Path(args.target).expanduser().resolve()
    with tempfile.TemporaryDirectory(prefix='ai-workbench-workflow-') as td:
        source = Path(td)
        extract_bundle(source)
        cmd = [sys.executable, str(source / 'install.py'), str(target)]
        if args.force:
            cmd.append('--force')
        if args.dry_run:
            cmd.append('--dry-run')
        return subprocess.call(cmd)


if __name__ == '__main__':
    raise SystemExit(main())
