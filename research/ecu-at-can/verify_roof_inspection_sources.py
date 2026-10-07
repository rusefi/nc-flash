"""Verify retained roof inspection sources; optionally reproduce PDF excerpt.

Artifact integrity only. No controller, CAN, electrical or vehicle simulation.
The five selected pages preserve evidence from the larger 2007 compilation.
"""
import argparse
import hashlib
import json
from pathlib import Path
import pymupdf

ROOT = Path(__file__).resolve().parent
MANUAL_SHA = '54e48bca00ddb5819fa0871740fff9e3aeaeceb34ef512deaf5a50e713315f9e'
PAGES = [1169, 1170, 1183, 1185, 1186]


def sha(data): return hashlib.sha256(data).hexdigest()


def excerpt(source):
    assert sha(source.read_bytes()) == MANUAL_SHA
    src = pymupdf.open(source); assert len(src) == 2348
    out = pymupdf.open()
    for n in PAGES: out.insert_pdf(src, from_page=n, to_page=n, links=False)
    return out.tobytes(garbage=4, deflate=True, no_new_id=True)


def main():
    p = argparse.ArgumentParser(); p.add_argument('--manual', type=Path)
    args = p.parse_args()
    manifest = json.loads((ROOT/'sources/mazda-2008-prht-inspection.json').read_text())
    count = 0
    for doc in manifest['documents']:
        for item in [doc] + doc['images']:
            data = (ROOT/'sources'/item['file']).read_bytes()
            assert len(data) == item['bytes'] and sha(data) == item['sha256'], item['file']
            count += 1
    m = json.loads((ROOT/'sources/mazda-prht-inspection-crosscheck.json').read_text())
    for item in m['artifacts']:
        b = (ROOT/'sources'/item['file']).read_bytes()
        assert len(b) == item['bytes'] and sha(b) == item['sha256'], item['file']
    pdf = ROOT/'sources/mazda-2007-prht-inspection-excerpt.pdf'
    doc = pymupdf.open(pdf); assert len(doc) == len(PAGES)
    assert '3O' in doc[1].get_text() and 'Closed position' in doc[1].get_text()
    assert 'PTC' in doc[2].get_text()
    if args.manual:
        assert excerpt(args.manual) == pdf.read_bytes(), 'Excerpt differs; check PyMuPDF version'
    print(f'Verified {count} HTML/image sources, {len(m["artifacts"])} PDF artifacts; '
          f'excerpt reproduction={bool(args.manual)}; PyMuPDF {pymupdf.VersionBind}')


if __name__ == '__main__': main()
