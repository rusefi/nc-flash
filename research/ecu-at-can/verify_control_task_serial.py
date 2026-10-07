"""Independent ISA, SCI0 exchange and initialization checks against original ROM.

Status/reply samples are explicit synthetic fixtures, never remote firmware.
"""
from collections import deque
import hashlib
import itertools
import json
from pathlib import Path
from sh_control_task_serial import TaskSerial
from verify_control_task_arithmetic import signed_bytes
from verify_control_raw_inputs import application
from verify_control_contributions import ECU

ROOT = Path(__file__).resolve().parent
PG, PH, SCR, SSR, TDR, RDR = [0xFFFF0000+a for a in [0xF764,0xF72C,0xF002,0xF004,0xF003,0xF005]]


def trace(command, reply, pg, status=0xC0):
    return [('read',PG,pg,2),('write',PG,pg & ~1,2),
            ('read',SSR,status,1),('write',SSR,(status & 0x87)|0x80,1),
            ('write',TDR,command & 255,1),('read',SSR,status,1),
            ('write',SSR,(status & 0x7F)|0x78,1),('read',SSR,status,1),
            ('read',RDR,reply,1),('read',SSR,status,1),
            ('write',SSR,(status & 0xBF)|0xB8,1),
            ('read',PG,pg & ~1,2),('write',PG,pg|1,2)]


def main():
    counts = dict(xtrct=0, addv=0, dt=0, original_add=0, exchange=0, initialize=0, rejections=0)
    values = [0,1,2,65535,65536,0x7FFFFFFF,0x80000000,0x80000001,0xFFFFFFFE,0xFFFFFFFF]
    for a,b,n,m,t,opcode in itertools.product(values,values,[0,4,15],[0,5,15],[0,1],[0x200D,0x300F]):
        e=TaskSerial();e.rom=(opcode | n<<8 | m<<4).to_bytes(2,'big')
        e.r[n]=a;e.r[m]=b;e.sr=0x3F0|t;want=e.r.copy()
        if opcode==0x200D:
            pair=want[m].to_bytes(4,'big')+want[n].to_bytes(4,'big')
            want[n]=int.from_bytes(pair[2:6],'big'); sr=0x3F0|t;key='xtrct'
        else:
            total=signed_bytes(want[n])+signed_bytes(want[m])
            want[n]=total % 2**32;sr=0x3F0|int(not -(2**31)<=total<2**31);key='addv'
        e.instruction(0)
        assert e.r==want and e.sr==sr
        counts[key]+=1
    for value,n,t in itertools.product(values,range(16),[0,1]):
        e=TaskSerial();e.rom=(0x4010|n<<8).to_bytes(2,'big');e.r[n]=value;e.sr=0x3F0|t
        want=e.r.copy();want[n]=(value-1) % 2**32
        e.instruction(0)
        assert e.r==want and e.sr==0x3F0|int(value==1)
        counts['dt']+=1
    for a,b in itertools.product(values,values):
        e=TaskSerial();e.r[5]=b;before=e.r[8:16].copy()
        want=max(-(2**31),min(2**31-1,signed_bytes(a)+signed_bytes(b))) % 2**32
        assert e.run(0x2034,a)==want and e.r[8:16]==before
        counts['original_add']+=1
    for reply,command,pg in itertools.product(range(256),[0,0x55,255,0x12345],[0,15]):
        e=TaskSerial();e.sci0_status=0xC0;e.sci0_rx.append(reply);e.registers[PG]=pg
        preserved=e.r[8:16].copy();ram=application(e)
        result=e.run(0x786E,command)
        assert result==int.from_bytes(bytes([reply]),'big',signed=True)&0xFFFFFFFF
        assert e.r[8:16]==preserved and e.sr==0xF0 and application(e)==ram
        assert e.accesses==trace(command,reply,pg) and e.sci0_tx==[command&255] and not e.sci0_rx
        counts['exchange']+=1
    for mode,scr,ph,pg in itertools.product([0,1,2,255,256,257], [0,0x55,0xAA,255], [0,0xA55A,65535], [0,15]):
        e=TaskSerial();e.sci0_status=0xC0;e.sci0_rx.append(0xA5)
        e.registers.update({SCR:scr,PH:ph,PG:pg});before=e.r[8:16].copy();ram=application(e)
        finalph=(ph&0x3FFF)|(0 if mode&255==0 else 0x4000 if mode&255==1 else 0x8000)
        intermediate=(ph&~0x4000)|(0x4000 if mode&255==1 else 0)
        want=[('read',SCR,scr,1),('write',SCR,scr&11,1),('write',0xFFFFF000,128,1),
              ('read',SCR,scr&11,1),('write',SCR,scr&8,1),('write',0xFFFFF006,242,1),
              ('write',0xFFFFF001,4,1),('read',PH,ph,2),('write',PH,intermediate,2),
              ('read',PH,intermediate,2),('write',PH,finalph,2),
              ('read',SCR,scr&8,1),('write',SCR,(scr&8)|48,1)]+trace(255,0xA5,pg)
        assert e.run(0x76B4,mode)==0xFFFFFFA5
        assert e.r[8:16]==before and e.sr==0xF0 and application(e)==ram
        assert e.accesses==want and not e.sci0_rx and e.sci0_tx==[255]
        counts['initialize']+=1
    for operation,address,size in [('read',SSR,1),('read',RDR,1),('write',RDR,1),
                                    ('read',SSR,2),('write',SSR,2),('write',PG,1),('read',0xFFFFF007,1)]:
        e=TaskSerial()
        try:
            if operation=='read':e.read(address,size)
            else:e.write(address,0,size)
        except ValueError:counts['rejections']+=1
        else:raise AssertionError('Missing expected bounded rejection')
    e=TaskSerial();e.sci0_status=0xC0;e.write(SSR,0,1);assert e.read(SSR,1)==0xC0
    e.write(PG,0xFFFF,2);assert e.read(PG,2)==15
    e=TaskSerial();e.sci0_status=0x80;e.sci0_rx.append(0xA5)
    try:e.run(0x786E,255,limit=2000)
    except RuntimeError:assert e.sci0_tx==[255]
    else:raise AssertionError('Missing RDRF should stay in original polling loop')
    assert len(e.sci0_rx)==1 and not any(a==RDR for _,a,_,_ in e.accesses)
    e=TaskSerial();e.timer_samples=deque([0xFFFFFFFF,0,1])
    assert [e.read(0xFFFFF430,4) for _ in range(3)]==[0xFFFFFFFF,0,1]
    for size in [4,2]:
        try:e.read(0xFFFFF430,size)
        except ValueError:counts['rejections']+=1
        else:raise AssertionError('Empty timer samples or wrong width admitted')
    result=dict(rom_sha256=hashlib.sha256(ECU).hexdigest(),checks=counts,
                not_ready_bounded_loop=True,scope=__doc__)
    (ROOT/'control-task-serial-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(counts)


if __name__=='__main__':main()
