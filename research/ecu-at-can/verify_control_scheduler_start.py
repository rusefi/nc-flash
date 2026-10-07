"""Independent stock mode0 3DD8 initialization through first task17 RTE.

Synthetic caller stack isolates temporary call storage; original selected-task
stack/PC/SR come from ROM. Stops at DCF8 before task17 initialization body.
"""
import hashlib,json,random
from pathlib import Path
from sh_control_interrupt import ControlInterrupt,execute_to
from verify_control_contributions import ECU,r,w
from verify_control_raw_inputs import application,expected_write
from verify_control_event2_activation import difference


def model(e):
    want=application(e)
    changes=[(0x12B0,4,1),(0x12B1,0,1),(0x12B4,17,2),(0x12B6,17,2),
        (0x12B8,0,4),(0x12BC,0xFFFF11A8,4),(0x12C0,0xB0,4),
        (0x12C4,0xFFFF1230,4),(0x12C8,0x41E0,4),
        (0x12D0,0x4204,4),(0x12D4,0xFFFF1240,4),(0x12DC,0,1),(0x12DD,0,1),
        (0x12F0,0x406D,4),(0x45CC,17,2)]
    for address in range(0x12E0,0x12F0):changes.append((address,0,1))
    changes.append((0x12E0,17,1))
    for address in range(0x129A,0x12AB,4):changes.append((address,65535,2))
    changes.extend([(0x129A,0,2),(0x129C,0,2),(0x1240,0,2),
        (0x12AA,38,2),(0x12AC,38,2),(0x128C,17,2)])
    for index in range(19):
        row=0x40D0+index*16
        address=int.from_bytes(ECU[row+4:row+8],'big')-0xFFFF0000
        changes.extend([(address,0,1),(address+2,255,1),(address+3,ECU[row+12]-int(index in [0,17]),1)])
    changes.extend([(0x1231,4,1),(0x1234,0xFFFF11A8,4),(0x11A0,0xDCF8,4),(0x11A4,0,4)])
    for address,value,size in changes:expected_write(want,address,value,size)
    return want


def main():
    count=0
    for seed in range(128):
        e=ControlInterrupt();rng=random.Random(seed);e.r[15]=0xFFFED000;e.r[4]=0;e.sr=0xB0
        for address in range(0x11A0,0x1300):w(e,address,rng.randrange(256))
        w(e,0x45CC,rng.randrange(65536),2)
        want=model(e)
        assert execute_to(e,0x3DD8,{0xDCF8},100000)==0xDCF8
        actual=application(e)
        if actual!=want:
            out=dict(seed=seed,difference=difference(e,want))
            Path(__file__).with_name('control-scheduler-start-oracle-limit.json').write_text(json.dumps(out,indent=2)+'\n')
        assert actual==want,(seed,difference(e,want))
        assert e.r[15]==0xFFFF11A8 and e.sr==0
        assert e.rte_transfers==[dict(pc=0x3F3C,sp=0xFFFF11A0,target=0xDCF8,status=0,restored_sr=0)]
        count+=1
    result=dict(status='PASS',scope=__doc__,rom_sha256=hashlib.sha256(ECU).hexdigest(),
        original_cases=count,first_task=17,first_body=0xDCF8,stock_stack=0xFFFF11A8,
        queued_tasks=[0,17],selected_priority=4,context_mask=0xB0,
        limits='Mode0 admitted explicitly; no parent3A38/reset or task17body/hardware clock executed.')
    Path(__file__).with_name('control-scheduler-start-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result)


if __name__=='__main__':main()
