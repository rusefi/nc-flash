"""Independent SETT preservation checks for the isolated startup probe."""
import json
from pathlib import Path
from probe_control_application_initialize import Initialize


def main():
    for sr in range(1024):
        e=Initialize();e.rom=bytes.fromhex('0018');e.sr=sr
        e.r=[0xA5000000+i for i in range(16)]
        before=e.r.copy();ram=e.ram.copy();gbr=e.gbr;pr=e.pr;macl=e.macl
        assert e.instruction(0)==(2,False)
        assert e.sr==sr-(sr%2)+1 and e.r==before and e.ram==ram
        assert e.gbr==gbr and e.pr==pr and e.macl==macl and e.visited=={0}
    Path(__file__).with_name('control-initialize-isa-verification.json').write_text(json.dumps(dict(sett_cases=1024,source='Renesas SH-2E REJ09B0316-0200 section7.2.50; https://www.renesas.com/en/document/mah/sh-2e-software-manual',scope=__doc__),indent=2)+'\n')
    print('1024 SETT preservation cases passed')

if __name__=='__main__':main()
