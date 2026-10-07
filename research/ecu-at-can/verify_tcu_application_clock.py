"""Check retained application ISR records and independently enumerate all clocks.

Reuse independent CMT0 boundary and actual hold-entry model replays. Runtime
application RAM checks are differential against original1220A, with independent
profiling and existing command/pin models; not an oracle for every nested body.
"""
import hashlib
import json

from verify_tcu_clock_ratio import ROOT,check


def verify(name,count):
    rows,result=check(name,count,application=True)
    for call,row in enumerate(rows):
        n=call+1;compare=(2560*n)&65535;stamp=n*1000
        event=row['extra']['application_interrupt']
        assert event==dict(phase=call%8,index=[0,1,2,3,0,1,2,4][call%8],
            armed=True,latency=0,duration=10,mode_after=3,stage_after=2,
            phase_after=n&255,entries=['0x1220a','0x126ec','0x1e5f6'],
            accesses=[['read',0xFFFFF454,2,compare],['read',0xFFFFF442,2,compare],
                ['read',0xFFFFF6C0,4,stamp],['read',0xFFFFF460,2,1],
                ['read',0xFFFFF460,2,1],['write',0xFFFFF460,2,0],
                ['read',0xFFFFF454,2,compare],
                ['write',0xFFFFF454,2,(compare+2560)&65535],
                ['read',0xFFFFF6C0,4,stamp+100]],
            differential_application_ram_checked=True,registers_and_mmio_checked=True,
            independent_command_pin_boundaries=2)
    result.update(application_prefixes=count,independent_command_pin_boundaries=count*2,
        application_compare_wraps=sum(((n*2560)&65535)+2560>65535 for n in range(1,count+1)))
    return rows,result


def main():
    rows,prefix=verify('tcu-application-clock-prefix8.json',8)
    old=(ROOT/'tcu-cmt1-delivery-prefix8.json').read_bytes()
    assert old==(ROOT/'tcu-application-hook-reuse-prefix8.json').read_bytes()
    result=dict(status='PASS',scope=__doc__,prefix8=prefix,
        default_hooks_byte_identical=True,default_prefix_sha256=hashlib.sha256(old).hexdigest())
    full=ROOT/'tcu-application-clock-probe.json'
    if full.exists():
        longer,verified=verify(full.name,320)
        assert longer[:8]==rows
        result.update(full320=verified,exact_first8=True)
    (ROOT/'tcu-application-clock-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:{a:v[a] for a in ['task_pairs','application_prefixes',
        'cmt0_prefixes','cmt1_prefixes','capture_prefixes','actual_hold_whole_ram_checks',
        'independent_command_pin_boundaries','application_compare_wraps']}
        for k,v in result.items() if k in ['prefix8','full320']},indent=2))


if __name__=='__main__':main()
