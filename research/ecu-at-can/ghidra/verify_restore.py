"""Verify an independently reopened extraction against the saved project.

Run VerifyCanEvidence.java read-only on both live and restored programs first.
This check rejects incomplete or stale/missing/extra exports. It does not run
Ghidra or extract archives. Use --write-report only after both reopenings pass.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exports(path):
    files = {f.relative_to(path).as_posix(): sha(f)
             for f in path.rglob('*') if f.is_file()}
    for f in path.glob('*.readback.tsv'):
        assert 'DECOMPILE_INCOMPLETE' not in f.read_text(), f
    return files


def verify(restored):
    manifest = json.loads((ROOT / 'snapshot.json').read_text())
    assert sha(ROOT / manifest['archive']) == manifest['sha256']
    for directory in [ROOT / 'live', restored]:
        assert not list(directory.glob('*.lock*')), ('Project still open', directory)
        for name, expected in manifest['files'].items():
            assert sha(directory / name) == expected, (directory, name)
    annotations = [line.split('\t', 4)
                   for line in (ROOT / 'annotations.tsv').read_text().splitlines()
                   if line.strip() and not line.startswith('#')]
    counts = Counter(row[0] for row in annotations)
    expected_files = {f'{name}.readback.tsv' for name in counts}
    expected_files.update(f'{row[0]}__{row[3]}.c' for row in annotations
                          if row[1] == 'function')
    live, copy = exports(ROOT / 'decompiled'), exports(restored / 'exports')
    assert set(live) == expected_files, ('Live export set', set(live) ^ expected_files)
    assert set(copy) == expected_files, ('Restored export set', set(copy) ^ expected_files)
    assert live == copy, ('Different exports', [name for name in live if live[name] != copy[name]])
    for name, count in counts.items():
        lines = (restored / 'exports' / f'{name}.readback.tsv').read_text().splitlines()
        assert lines[-1] == f'verified_annotations\t{count}', name
        expected_rows = ['\t'.join([r[2], r[1], r[3]]) for r in annotations if r[0] == name]
        assert lines[4:-1] == expected_rows, ('Readback annotation rows', name)
    return dict(date=datetime.now(timezone.utc).date().isoformat(),
        archive_sha256=manifest['sha256'],
        restored_project_files_verified=len(manifest['files']),
        restored_annotations_verified=sum(counts.values()),
        identical_export_files=len(live), restored_programs=sorted(counts),
        method='Independent Ghidra read-only reopening; verify_restore.py checks '
               'archive/live/restored hashes, complete expected export sets, '
               'no incomplete readbacks, all annotation rows and identical exports.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('restored', type=Path)
    parser.add_argument('--write-report', action='store_true')
    args = parser.parse_args()
    result = verify(args.restored.resolve())
    data = json.dumps(result, indent=2) + '\n'
    if args.write_report:
        (ROOT / 'restore-verification.json').write_text(data)
    print(data, end='')


if __name__ == '__main__':
    main()
