"""Read-only aligned SH MOV.W/MOV.L literal leads for ECU INTC setup."""
import hashlib,json
from pathlib import Path
from verify_control_contributions import ECU


def main():
    words={v:[] for v in range(0xED00,0xED18,2)}
    longs={0xFFFF0000+v:[] for v in words}
    for pc in range(0,len(ECU)-4,2):
        opcode=int.from_bytes(ECU[pc:pc+2],'big')
        if opcode>>12==9:
            a=pc+4+(opcode&255)*2
            if a+2<=len(ECU):
                value=int.from_bytes(ECU[a:a+2],'big')
                if value in words:words[value].append(dict(pc=hex(pc),pool=hex(a)))
        if opcode>>12==13:
            a=((pc+4)&~3)+(opcode&255)*4
            if a+4<=len(ECU):
                value=int.from_bytes(ECU[a:a+4],'big')
                if value in longs:longs[value].append(dict(pc=hex(pc),pool=hex(a)))
    branches=[]
    for pc in range(0,len(ECU)-2,2):
        opcode=int.from_bytes(ECU[pc:pc+2],'big')
        if opcode>>12 in [10,11]:
            displacement=opcode&4095
            if displacement&2048:displacement-=4096
            target=pc+4+displacement*2
            if target in [0xAA4A,0xAA94,0xF758,0x3DD8]:
                branches.append(dict(pc=hex(pc),target=hex(target),kind='BSR' if opcode>>12==11 else 'BRA'))
    data=dict(relative_branch_candidates=branches,scope=__doc__,rom_sha256=hashlib.sha256(ECU).hexdigest(),
        word_loads={hex(k):v for k,v in words.items() if v},
        long_loads={hex(k):v for k,v in longs.items() if v},
        limits='Aligned opcode-shaped bytes may be data; base+offset and computed address patterns can be missed.')
    Path(__file__).with_name('control-interrupt-priority-leads.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(data,indent=2))


if __name__=='__main__':main()
