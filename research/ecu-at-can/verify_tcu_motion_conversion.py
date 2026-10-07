"""Original22DDC stock conversion in the nonnegative source domain.

The observed producers clamp80EA/91A2 to0..32767. This checks selected boundary
and deterministic random inputs, not every source pair, other calibrations,
negative/out-of-domain inputs, physical units or all soft-float helpers.
"""
import hashlib
import json
import random
from pathlib import Path

from sh_rotate import SHRotate
from verify_can201_byte6 import TCU, r, w
from verify_tcu_base_publication import ram

ROOT = Path(__file__).resolve().parent


def converted(value):
    assert 0 <= value <= 32767
    # Stock coefficient: trunc(299*9651/4100)=703, then unsigned *1000/1000.
    # Nonnegative product <2**25 is exact in binary64; division by256 is exact.
    return min(0xFF00, value*703//256)


def model(t):
    a, b = [converted(r(t,p,2)) for p in [0x80EA,0x91A2]]
    for address, value, size in [(0x932C,a,2),(0x932E,b,2),(0x800E,a>>8,1),
                                 (0x80A4,a*10//256,2),(0x80BA,b*10//256,2),
                                 (0xA4FC,r(t,0xA4FA),1)]:
        w(t,address,value,size)


def main():
    assert hashlib.sha256(TCU).hexdigest()=='8fb064e91dd2590a30189d70874f5607350812e6c8f98f6e4a132085c4a808d6'
    assert [int.from_bytes(TCU[a:a+2],'big') for a in [0x76E78,0x76E7A,0x76E7C]] == [299,4100,1000]
    assert int.from_bytes(TCU[0x22E62:0x22E64],'big') == 9651
    limit = (0xFF00*256+702)//703
    edges = [0,1,93,94,127,128,255,256,3070,7017,14446,limit-1,limit,limit+1,32766,32767]
    rng = random.Random(0x22DDC)
    pairs = [(a,b) for a in edges for b in edges]
    pairs += [(rng.randrange(32768),rng.randrange(32768)) for _ in range(256)]
    for index,(a,b) in enumerate(pairs):
        t=SHRotate(TCU)
        for address,value,size in [(0x80EA,a,2),(0x91A2,b,2),(0x9330,index&255,1),
                 (0xA4FA,(index*31)&255,1),(0x932C,0xA55A,2),(0x932E,0x5AA5,2),
                 (0x800E,0xCC,1),(0x80A4,0xABCD,2),(0x80BA,0xFEDC,2),(0xA4FC,0xEF,1)]:
            w(t,address,value,size)
        ref=SHRotate(TCU); ref.ram=dict(t.ram); model(ref)
        t.run(0x22DDC,limit=200000)
        assert ram(t)==ram(ref),(index,a,b,{hex(k):(ram(t).get(k),ram(ref).get(k)) for k in ram(t).keys()|ram(ref).keys() if ram(t).get(k)!=ram(ref).get(k)})
    result=dict(status='PASS',scope=__doc__,whole_application_ram_cases=len(pairs),
                selector_bytes=256,coefficient=703,first_capped_input=limit,
                source_domain=[0,32767],rom_sha256=hashlib.sha256(TCU).hexdigest())
    (ROOT/'tcu-motion-conversion-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
