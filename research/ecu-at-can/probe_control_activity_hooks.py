"""Trace original callback descriptor admission during retained outer event calls."""
import hashlib
import json
from pathlib import Path
from probe_control_outer_event import Outer
from verify_control_contributions import ECU,r

ROOT=Path(__file__).resolve().parent

class Hooks(Outer):
    def __init__(self):
        super().__init__();self.descriptors=[];self.counter_writes=[]

    def instruction(self,pc):
        if pc==0xDAE8:
            bank=self.r[4]&255;index=self.r[5]&65535
            base=self.read(0x112E8+bank*4,4);address=base+index*8
            self.descriptors.append(dict(pr=self.pr,bank=bank,index=index,address=address,
                selector=self.read(address,2),words=self.read(address+2,2),target=self.read(address+4,4),tail=self.tail.copy()))
        return super().instruction(pc)

    def write(self,a,v,size):
        if 0xFFFF660E<=a<0xFFFF6612:
            self.counter_writes.append(dict(pc=self.pc,pr=self.pr,address=a,value=v,size=size))
        return super().write(a,v,size)


def main():
    e=Hooks();e.registers[0xFFFFF74E]=1;e.run(0xCA94);e.write(0xFFFFD800,2,4)
    rows=[]
    for i in range(10):
        start=len(e.descriptors);write_start=len(e.counter_writes)
        e.run(0x2BCE6,0xFFFFD800,limit=1000000)
        rows.append(dict(call=i,phase=r(e,0x651C),descriptors=e.descriptors[start:],writes=e.counter_writes[write_start:]))
    (ROOT/'control-activity-hooks-probe.json').write_text(json.dumps(dict(rom_sha256=hashlib.sha256(ECU).hexdigest(),scope=__doc__,rows=rows),indent=2)+'\n')
    for row in rows:print(row['call'],[(hex(d['pr']),d['index'],hex(d['target'])) for d in row['descriptors']])

if __name__=='__main__':main()
