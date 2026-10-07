"""Render the three saved 2008 Mazda PRHT SWF schematics with FFDec.

The source manifest pins the downloaded originals. Only frame 1 is the
unobstructed schematic; later frames contain interactive viewer overlays.
This exports the document, not an execution model of the roof controller.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jar', type=Path, required=True, help='FFDec26.3.0 ffdec.jar')
    args = parser.parse_args()
    manifest_path = ROOT / 'sources/mazda-2008-prht-wiring-swf.json'
    manifest = json.loads(manifest_path.read_text())
    outputs = []
    for letter in 'abc':
        name = f'mazda-2008-prht-wiring-0916-{letter}'
        source = ROOT / 'sources' / (name + '.swf')
        expected = next(row for row in manifest['sources'] if row['local_file'].endswith(source.name))
        assert hashlib.sha256(source.read_bytes()).hexdigest() == expected['sha256']
        # Scratch is reproducible; only the resulting schematic is durable.
        with tempfile.TemporaryDirectory(prefix='nc-roof-wiring-') as scratch:
            command = ['java', '-Djava.awt.headless=true', '-jar', str(args.jar.resolve()),
                       '-select', '1', '-zoom', '2', '-format', 'frame:png',
                       '-export', 'frame', scratch, str(source)]
            result = subprocess.run(command, text=True, capture_output=True, check=True)
            assert 'v.26.3.0' in result.stdout and 'Exported frame 1/1' in result.stdout
            assert result.stdout.rstrip().endswith('OK'), result.stdout
            assert 'Exception' not in result.stderr and 'ERROR' not in result.stderr, result.stderr
            output = ROOT / 'sources' / (name + '.png')
            shutil.copyfile(Path(scratch) / '1.png', output)
        data = output.read_bytes()
        assert data.startswith(b'\x89PNG\r\n\x1a\n')
        assert [int.from_bytes(data[i:i+4], 'big') for i in [16, 20]] == [1620, 1180]
        outputs.append(dict(local_file=str(output.relative_to(ROOT)), bytes=len(data),
                            sha256=hashlib.sha256(data).hexdigest(), frame=1,
                            width=1620, height=1180, renderer='FFDec26.3.0 native PNG, zoom2'))
    manifest['rendered'] = outputs
    manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')
    print('Verified source hashes and exported', len(outputs), 'schematics')


if __name__ == '__main__':
    main()
