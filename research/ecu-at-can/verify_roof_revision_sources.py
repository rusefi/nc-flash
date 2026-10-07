"""Verify saved documentary inputs and the specific indicator-row discrepancy.

This checks source identity/text, not controller execution or roof behavior.
Optional --download restores only the seven already identified public assets.
"""
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import urllib.request

import pymupdf

ROOT = Path(__file__).resolve().parent / 'sources'


class Rows(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows = []
        self.row = None
        self.cell = None

    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            self.row = []
        elif tag in ('td', 'th'):
            self.cell = []

    def handle_data(self, text):
        if self.cell is not None:
            self.cell.append(text)

    def handle_endtag(self, tag):
        if tag in ('td', 'th') and self.cell is not None:
            if self.row is not None:
                self.row.append(' '.join(' '.join(self.cell).split()))
            self.cell = None
        elif tag == 'tr' and self.row is not None:
            self.rows.append(self.row)
            self.row = None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--download', action='store_true')
    args = parser.parse_args()
    manifest = json.loads((ROOT / 'mazda-d9g4-prht-crosscheck.json').read_text())
    for artifact in manifest['artifacts']:
        path = ROOT / artifact['file']
        if args.download:
            data = urllib.request.urlopen(artifact['url'], timeout=30).read()
            assert hashlib.sha256(data).hexdigest() == artifact['sha256'], 'Remote content changed; keep saved evidence'
            path.write_bytes(data)
        data = path.read_bytes()
        assert len(data) == artifact['bytes']
        assert hashlib.sha256(data).hexdigest() == artifact['sha256']
        if path.suffix == '.html':
            assert b'D9G4-1A-22C_Ver17' in data
        else:
            assert data.startswith(b'\x89PNG\r\n\x1a\n')
    comparison = manifest['comparison']
    path = ROOT / comparison['file']
    assert path.stat().st_size == comparison['bytes']
    assert hashlib.sha256(path.read_bytes()).hexdigest() == comparison['sha256']
    with pymupdf.open(path) as pdf:
        text = ' '.join(pdf[comparison['pdf_page_zero_based']].get_text().split())
    assert 'Top lock is locked after close operation is finished.' in text
    assert 'Power retractable hardtop switch is turned on.' in text
    parsed = Rows()
    parsed.feed((ROOT/'mazda-d9g4-prht-function.html').read_text())
    rows = [row for row in parsed.rows if row and row[0] == 'Power retractable hardtop half-open and not operating']
    assert len(rows) == 1 and len(rows[0]) == 4
    assert rows[0][-1] == '• Open operation is finished. • Close operation is finished.'
    assert 'temporarily stopped' in rows[0][-2]
    print('Verified7 saved mirror assets + original PDF; distinct paused-indicator rows confirmed. No behavioral proof.')


if __name__ == '__main__':
    main()
