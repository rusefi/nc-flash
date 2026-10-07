"""Original stop-entry decisions, progress counters and hold-flag producer.

Terminal bodies are not stubbed: a distinct observation exception stops at
their entry, so terminal-route cases are not counted as complete returns.
Core monitor state has independent oracles; auxiliary AA590 effects execute
but are outside that state oracle. Explicit TCNT0 samples, no physical peer.
"""
from collections import deque
import itertools
import json
import hashlib
from pathlib import Path
from sh_control_task_serial import TaskSerial
from verify_control_contributions import ECU,w,r
from verify_control_raw_inputs import application,expected_write

ROOT=Path(__file__).resolve().parent
FIELDS={0x6604:1,0x6605:1,0x6606:1,0x6608:4,0x660C:2,
        0x660E:1,0x660F:1,0x6610:1,0x6611:1,0x2110:2,0x3FF9:1,
        0x735C:1,0x722A:1}


class TerminalEntry(Exception):pass


class StopProbe(TaskSerial):
    def __init__(self):
        super().__init__();self.stop=None;self.helpers=[]
        self.timer_samples=deque(range(4096));self.sci0_status=0xC0
    def instruction(self,pc):
        if pc in [0xF8D6,0xF972]:
            self.stop=pc
            raise TerminalEntry
        if pc in [0xAA580,0xAA590]:self.helpers.append(pc)
        return super().instruction(pc)


def core(e):return {a:r(e,a,n) for a,n in FIELDS.items()}


def monitor_model(e):
    want=core(e);target=None;helpers=[]
    if want[0x735C]==1:
        if want[0x6605]==0:
            want.update({0x3FF9:0x5A,0x660C:0,0x6606:1})
        else:
            want[0x2110]=0x00FF;target=0xF972;helpers=[0xAA580,0xAA590]
    elif want[0x6605]==0:
        if want[0x660C]>=8:want.update({0x6605:1,0x6608:0,0x6604:1})
        want[0x660C]=(want[0x660C]+1)&65535
    else:
        want[0x6608]=min(0xFFFFFFFF,want[0x6608]+1)
        done=(want[0x660E]<=want[0x660F] and want[0x6610]<=want[0x6611])
        if want[0x6608]>=72000 or (want[0x6608]>=8 and done):
            want.update({0x6605:2,0x2110:0x01FE,0x6606:0,0x3FF9:0})
            target=0xF8D6;helpers=[0xAA590]
    return want,target,helpers


def monitor(e,entry=0x2C4FC):
    want,target,helpers=monitor_model(e);saved=e.r[8:16].copy()
    try:e.run(entry,limit=100000)
    except TerminalEntry:assert target==e.stop
    else:assert target is None and e.r[8:16]==saved
    assert core(e)==want,(core(e),want)
    assert e.helpers==helpers and e.sr&0xF0==0xF0
    return target


def main():
    assert int.from_bytes(ECU[0xBAE38:0xBAE3A],'big')==8
    assert int.from_bytes(ECU[0xBAE3C:0xBAE40],'big')==72000
    assert ECU[0xBB25C]==2
    counts=dict(publisher=0,increments=0,producer=0,initializer=0,monitor=0,monitor_returned=0,
                monitor_terminal=0,gate=0,gate_returned=0,gate_terminal=0)
    for lo,hi in itertools.product(range(256),[0,255]):
        e=StopProbe();sample=(hi<<8)|lo;w(e,0x44A2,sample,2);w(e,0x722A,0xA55A,2)
        want=application(e);flag=sample&1
        expected_write(want,0x722A,(flag<<8)|(flag^255),2)
        saved=e.r[8:16].copy();e.run(0x4105C)
        assert application(e)==want and e.r[8:16]==saved
        counts['publisher']+=1
    hooks={0x1616C:0x660E,0x16178:0x660F,0x16172:0x6610,0x1617E:0x6611}
    for (entry,address),old in itertools.product(hooks.items(),range(256)):
        e=StopProbe();w(e,address,old);want=application(e);saved=e.r[8:16].copy()
        expected_write(want,address,(old+1)&255,1);e.run(entry)
        assert application(e)==want and e.r[8:16]==saved and e.sr&0xF0==0xF0
        counts['increments']+=1
    for old,source in itertools.product(range(256),[0,1,2,255]):
        e=StopProbe();w(e,0x7358,old);w(e,0x722A,source);w(e,0x735C,255)
        want=application(e);value=2 if source==1 else max(0,old-1)
        expected_write(want,0x7358,value,1);expected_write(want,0x735C,int(value!=0),1)
        saved=e.r[8:16].copy();e.run(0x42AA2)
        assert application(e)==want and e.r[8:16]==saved
        counts['producer']+=1
    for old in range(256):
        e=StopProbe();w(e,0x6605,old);w(e,0x6606,old);want=application(e)
        expected_write(want,0x6605,0,1);expected_write(want,0x6606,1,1)
        e.run(0x2C468);assert application(e)==want;counts['initializer']+=1
    pairs=[(0,0,0,0),(1,0,0,0),(0,0,1,0),(127,128,255,255),(128,127,0,0)]
    for mode,state,warm,age,pair in itertools.product([0,1,2],[0,1,2],
            [0,7,8,65535],[0,6,7,71999,0xFFFFFFFF],pairs):
        e=StopProbe()
        for a,v in [(0x735C,mode),(0x6605,state),(0x660C,warm),(0x6608,age),
                    (0x6604,255),(0x6606,255),(0x3FF9,0xA5),(0x2110,0xA55A)]:w(e,a,v,FIELDS[a])
        for a,v in zip([0x660E,0x660F,0x6610,0x6611],pair):w(e,a,v)
        target=monitor(e);counts['monitor']+=1
        counts['monitor_terminal' if target else 'monitor_returned']+=1
    for source,pair in itertools.product(range(256),pairs):
        e=StopProbe();w(e,0x722A,source)
        for a,v in zip([0x660E,0x660F,0x6610,0x6611],pair):w(e,a,v)
        want=application(e);saved=e.r[8:16].copy()
        target=0xF972 if source==1 else None if pair[0]>pair[1] or pair[2]>pair[3] else 0xF8D6
        try:e.run(0x2C5DE)
        except TerminalEntry:assert e.stop==target
        else:assert target is None and e.r[8:16]==saved
        assert application(e)==want
        counts['gate']+=1;counts['gate_terminal' if target else 'gate_returned']+=1
    result=dict(rom_sha256=hashlib.sha256(ECU).hexdigest(),checks=counts,scope=__doc__)
    (ROOT/'control-task-stop-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(counts)


if __name__=='__main__':main()
