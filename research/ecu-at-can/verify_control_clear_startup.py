"""Original DMA RAM clear, filtered-input initialization, application, and tasks.

Explicit sequence of original routines is consistent with identified startup
fragments; the full joining reset/board caller chain is not executed here.
"""
import hashlib
import json
from pathlib import Path
from verify_control_initialized_activity import InitializedActivity, fields
from verify_control_raw_inputs import application, expected_write
from verify_control_contributions import ECU, r


def run_sequence(entry=0x100D8, filename='control-clear-startup-verification.json',
                 scope=__doc__, samples=None, machine_type=InitializedActivity):
    samples = [1]*10 if samples is None else samples
    e=machine_type();e.registers[0xFFFFF74E]=1
    # Nonzero every byte in the candidate block, plus guards outside it.
    for address in range(0xFFFF3FFC,0xFFFFBFA4):e.write(address,(address*37)%255+1,1)
    want=application(e)
    for address in range(0x4000,0xBFA0):expected_write(want,address,0,1)
    row=dict(scope=scope,entry=entry,rom_sha256=hashlib.sha256(ECU).hexdigest(),before=fields(e),tasks=[])
    try:
        e.stage='clear';saved=e.r[8:16].copy();gbr=e.gbr
        e.run(entry,limit=2000000)
        assert application(e)==want and e.r[8:16]==saved and e.gbr==gbr
        row['cleared']=fields(e)
        e.stage='filter';e.run(0xCA94)
        assert r(e,0x44A2,2)&1==1
        row['filtered']=fields(e)
        e.stage='initializer';saved=e.r[8:16].copy();gbr=e.gbr
        e.run(0x1619A,limit=2000000)
        assert e.r[8:16]==saved and e.gbr==gbr and not e.activity_pending
        row['initialized']=fields(e)
        assert r(e,0x9158,2)==0 and r(e,0x915E)==0 and r(e,0x915C)==0
        assert r(e,0x8FD4,2)==640 and r(e,0x9125)==1
        e.stage='fixture';e.write(0xFFFFD800,2,4)
        previous=1
        for call,value in enumerate(samples):
            e.stage=f'event2-{call}';saved=e.r[8:16].copy();gbr=e.gbr
            if value!=previous:
                e.registers[0xFFFFF74E]=(e.registers[0xFFFFF74E]&~1)|value
                e.run(0xCADE);e.run(0xCADE)
                assert r(e,0x44A2,2)&1==value
            previous=value
            e.run(0x2BCE6,0xFFFFD800,limit=1000000)
            assert e.r[8:16]==saved and e.gbr==gbr and not e.activity_pending
            row['tasks'].append(fields(e))
        assert len(e.activity_checked)==1+5*((len(samples)+4)//5)
        if all(value==1 for value in samples):
            assert all(t['0x735c']==1 and t['0x9158']==0 and t['0x915e']==0 for t in row['tasks'])
        row['status']='returned'
    except (ValueError,RuntimeError,NotImplementedError,AssertionError) as exc:
        row.update(status=type(exc).__name__+': '+str(exc),stage=e.stage,pc=e.pc,tail=e.tail)
    row.update(dma=e.dma_transfers,checked=e.activity_checked,bank=e.bank_checked,writes=e.activity_writes)
    row['samples']=samples
    Path(__file__).with_name(filename).write_text(json.dumps(row,indent=2)+'\n')
    print(row['status'],'task returns',len(row['tasks']),'activity boundaries',len(e.activity_checked))
    assert row['status']=='returned'
    return e, row


if __name__=='__main__':run_sequence()
