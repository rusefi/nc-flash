"""Original TCU pin selection, command arbitration and complete task tail.

Explicit software port words; no electrical pins, output-driver identity,
clock, reset context or actuator model. Original nested helpers execute.
"""
import copy
import hashlib
import itertools
import json
import random
from pathlib import Path
import verify_tcu_timer_configuration as setup
from verify_tcu_timer_configuration import TCU,w,r,execute

ROOT=Path(__file__).resolve().parent
assert TCU[0x5C500:0x5C508].hex()=='fffff74e0e000000'


class PinRegisters(setup.ConfigurationRegisters):
    def read(self,address,size):
        if address in [0xFFFFF748,0xFFFFF74A,0xFFFFF74C,0xFFFFF74E]:
            if size!=2:raise ValueError('Pin word width')
            a=address-0xFFFF0000;value=self.configuration[a]
            self.configuration_trace.append(('read',a,2,value));return value
        return super().read(address,size)
    def write(self,address,value,size):
        if address in [0xFFFFF748,0xFFFFF74A,0xFFFFF74C,0xFFFFF74E]:
            if size!=2:raise ValueError('Pin word width')
            a=address-0xFFFF0000;value &= 65535;self.configuration[a]=value
            self.configuration_trace.append(('write',a,2,value));return
        super().write(address,value,size)


def fixture(seed=0):
    t=setup.fixture(seed);t.__class__=PinRegisters
    rng=random.Random(seed^0x185F8)
    for a in [0xF748,0xF74A,0xF74C,0xF74E]:t.configuration[a]=rng.randrange(65536)
    for a in [0x8A18,0x8A19,0xA5A0,0xA5A1,0xA5A2]:w(t,a,rng.randrange(256))
    return t


def modify(t,a,mask,bits):
    old=t.configuration[a];new=(old&mask)|bits
    t.configuration_trace.extend([('read',a,2,old),('write',a,2,new)])
    t.configuration[a]=new


def switch_model(t,disable):
    if disable:
        modify(t,0xF730,65535,15);modify(t,0xF734,0xFFAA,0);modify(t,0xF738,0xFFF0,0)
    else:
        modify(t,0xF738,0xFFF0,0);modify(t,0xF730,65535,15);modify(t,0xF734,65535,0x55)


def descriptor_model(t,flag):
    modify(t,0xF74E,0xBFFF,0 if flag&1 else 0x4000)


def port_init_model(t):
    setup.model_writes(t,[(0xF748,2,0x4000),(0xF74A,2,0x8000),(0xF74C,2,0),(0xF74E,2,0)])


def bounded(t,begin,end,model):
    ref=copy.deepcopy(t);model(ref);sp=t.r[15];mask=t.sr&~0x301
    setup.execute_slice(t,begin,end)
    assert t.r[15]==sp and t.sr&~0x301==mask
    setup.equal(t,ref)


def command_model(t):
    value=int(r(t,0xA5A1)==1 or r(t,0xA5A2)==1)
    w(t,0xA5A0,value);w(t,0x8A18,value)


def dispatch_model(t):
    command,previous=r(t,0x8A18),r(t,0x8A19)
    if command==1:switch_model(t,True)
    elif command==0 and previous==1:switch_model(t,False)
    w(t,0x8A19,command);descriptor_model(t,int(command==1))


def checked(t,entry,model,argument=0):
    ref=copy.deepcopy(t);model(ref);execute(t,entry,argument);setup.equal(t,ref)


def tail(t):
    ref=copy.deepcopy(t);command_model(ref);dispatch_model(ref)
    # Actual1271A tail expects the enclosing126EC saved PR. Supply only that
    # ABI stack frame; preceding task body is not executed or inferred.
    saved=t.r[8:16].copy();macl=t.macl;sr=t.sr&~0x301
    t.r[15]-=4;t.write(t.r[15],0xFFFFFFF0,4)
    t.visited.clear();t.run(0x1271A,limit=300000)
    assert t.r[8:16]==saved and t.macl==macl and t.sr&~0x301==sr
    assert {0x529AC,0x1863C,0x185F8,0x141BC,0x1421A,0x1423E}<=t.visited
    setup.equal(t,ref)


def direct():
    counts=dict(switch=0,descriptor=0,dispatch=0,initialize=0,command=0,setter=0,task_tail=0,port_init=0,caller_slice=0,rejected=0)
    for seed in range(128):
        for disable in [False,True]:
            t=fixture(seed);checked(t,0x1574C if disable else 0x1576C,lambda q:switch_model(q,disable));counts['switch']+=1
    for flag,mask in itertools.product(range(256),[0,3,15]):
        t=fixture(flag+mask);t.sr=(t.sr&~0xF0)|(mask<<4);t.r[5]=flag
        checked(t,0x141BC,lambda q:descriptor_model(q,flag),0x5C500);counts['descriptor']+=1
    for command,previous in itertools.product(range(256),[0,1,2,255]):
        t=fixture(command+previous);w(t,0x8A18,command);w(t,0x8A19,previous)
        checked(t,0x185F8,dispatch_model);counts['dispatch']+=1
    for seed in range(32):
        t=fixture(seed);checked(t,0x147FE,port_init_model);counts['port_init']+=1
        t=fixture(seed);bounded(t,0x14912,0x14916,port_init_model);counts['caller_slice']+=1
        for begin,end in [(0x115AA,0x115BE),(0x115D4,0x115E8)]:
            t=fixture(seed)
            def system_request(q):w(q,0xA5A1,1);command_model(q);dispatch_model(q)
            bounded(t,begin,end,system_request);counts['caller_slice']+=1
        t=fixture(seed)
        def initialize(q):w(q,0x8A18,0);w(q,0x8A19,0);descriptor_model(q,0)
        checked(t,0x185E4,initialize);counts['initialize']+=1
        t=fixture(seed)
        def command_init(q):
            for a in [0xA5A0,0xA5A1,0xA5A2,0x8A18]:w(q,a,0)
        checked(t,0x52994,command_init);counts['initialize']+=1
    for first,second in itertools.product(range(256),[0,1,2,255]):
        t=fixture(first+second);w(t,0xA5A1,first);w(t,0xA5A2,second)
        checked(t,0x529AC,command_model);counts['command']+=1
        t=fixture(first+second);w(t,0xA5A1,second);w(t,0xA5A2,first)
        tail(t);counts['task_tail']+=1
    for selector,value in itertools.product(range(256),[0,1,2,255,0x1234]):
        t=fixture(selector+value);t.r[5]=value
        def setter(q):
            if selector in [0,1]:w(q,0xA5A1+selector,value&255)
        checked(t,0x529CE,setter,selector);counts['setter']+=1
    for value in [0,1,255,256,0x12345678,0xFFFFFFFF]:
        t=fixture(value);checked(t,0x1863C,lambda q:w(q,0x8A18,value&255),value);counts['setter']+=1
    t=fixture()
    for a,n,writing in [(0xFFFFF74E,1,False),(0xFFFFF74E,4,True),(0xFFFFF734,1,False),(0xFFFFF750,2,True)]:
        try:
            if writing:t.write(a,0,n)
            else:t.read(a,n)
        except ValueError:counts['rejected']+=1
        else:raise AssertionError('unsupported pin access')
    return counts


def retained():
    t=fixture(100);setup.configure(t);checked(t,0x147FE,port_init_model);rows=[]
    # Public two-source setter/arbitrator always produces binary commands.
    for call,(a,b) in enumerate([(0,0),(1,0),(1,1),(0,1),(0,0),(2,255),(1,2),(2,2)]*8,1):
        for selector,value in [(0,a),(1,b)]:
            t.r[5]=value;checked(t,0x529CE,lambda q:w(q,0xA5A1+selector,value),selector)
        t.configuration_trace=[];tail(t)
        rows.append(dict(call=call,sources=[a,b],command=r(t,0x8A18),previous=r(t,0x8A19),
                         ports={hex(a):t.configuration[a] for a in [0xF730,0xF734,0xF736,0xF738,0xF748,0xF74A,0xF74C,0xF74E]},trace=t.configuration_trace.copy()))
    # Direct nonbinary commands are tested separately: 1->2->0 does not
    # reselect PWM, unlike 1->0. This is not claimed reachable via529AC.
    t=fixture(200);setup.configure(t);nonbinary=[]
    for command in [0,1,2,0,1,0]:
        checked(t,0x1863C,lambda q:w(q,0x8A18,command),command)
        t.configuration_trace=[];checked(t,0x185F8,dispatch_model)
        nonbinary.append(dict(command=command,selection=t.configuration[0xF734],trace=t.configuration_trace.copy()))
    assert nonbinary[3]['selection']&0x55==0 and nonbinary[-1]['selection']&0x55==0x55
    return rows,nonbinary


def main():
    counts=direct();rows,nonbinary=retained();print(counts,'retained',len(rows),flush=True)
    result=dict(scope=__doc__,rom_sha256=hashlib.sha256(TCU).hexdigest(),counts=counts,retained=rows,nonbinary=nonbinary,
      limits='Original1271A tail with ABI frame, not full126EC/startup/taskadmission. Explicit portword latches; PBIR unchanged. No pin voltages, board/driver identity, physicalactuation or timing.')
    (ROOT/'tcu-output-pin-switch-verification.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':main()
