"""Original744C6 stock calibration flag bank, independently mapped RAM outputs.

No calibration mutation or physical interpretation. Whole application-RAM checks.
"""
import hashlib
import json
import random
from pathlib import Path
from probe_control_activity_hooks import Hooks
from verify_control_contributions import ECU,r,w
from verify_control_raw_inputs import application,expected_write

ROOT=Path(__file__).resolve().parent
CALIBRATIONS=list(range(0xE0CC2,0xE0CD1))+[0xE0CD2]+list(range(0xE0CD4,0xE0CDD))+[0xE0CD1,0xE0CDD,0xE0CDE,0xE0CE2,0xE0CE3,0xE0CE4,0xE0CDF,0xE0CE0,0xE0CE7,0xE0CD3,0xE0CE1,0xE0CE5,0xE0CE6]
MAPPING=dict(zip(range(0x911A,0x9140),CALIBRATIONS,strict=True))


def expected(e):
    want=application(e)
    for dest,source in MAPPING.items():expected_write(want,dest,int(ECU[source]==0),1)
    return want


def main():
    rng=random.Random(744006)
    for i in range(64):
        e=Hooks()
        for a in range(0x9110,0x9150):w(e,a,(i*4 if i<4 else rng.randrange(256)))
        want=expected(e);saved=e.r[8:16].copy();gbr=e.gbr
        e.run(0x744C6)
        assert application(e)==want and e.r[8:16]==saved and e.gbr==gbr and e.sr&0xF0==0xF0
        assert not e.accesses
    mapping=[dict(ram=hex(d),rom=hex(s),calibration=ECU[s],flag=int(ECU[s]==0)) for d,s in MAPPING.items()]
    result=dict(rom_sha256=hashlib.sha256(ECU).hexdigest(),scope=__doc__,whole_ram_cases=64,flag_count=len(MAPPING),mapping=mapping)
    (ROOT/'control-flag-bank-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print('64 whole-RAM cases;',len(MAPPING),'stock flag mappings;9125=',r(e,0x9125))

if __name__=='__main__':main()
