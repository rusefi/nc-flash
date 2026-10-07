"""Original BC00 two-byte SCI4 exchange with explicit ready/data samples."""
import itertools
import json
from pathlib import Path
from control_sci4_fixture import Serial4
from probe_control_timer_event2 import TimerEvent
from verify_control_raw_inputs import application


def main():
    cases=0
    for a,b,tx,control,pins in itertools.product([0,1,127,128,255],[0,1,255],
                                               [0,0x12FF],[0,8,48,255],[0,0xFFFF]):
        e=TimerEvent();e.r[15]=0xFFFED000;e.sr=0xF0;e.sci4=Serial4(0xC0,[a,b])
        e.sci4.config[0xFFFFF022]=control
        e.registers[0xFFFFF74E]=pins;e.registers[0xFFFFF75C]=pins&0x380
        saved=e.r[8:16].copy();gbr=e.gbr;memory=application(e)
        e.r[5]=tx&255;value=e.run(0xBC00,tx>>8)
        raw=(a<<8)|b;assert value==(raw if raw<32768 else raw|0xFFFF0000)
        assert application(e)==memory and e.r[8:16]==saved and e.gbr==gbr and e.sr&0xF0==0xF0
        assert not e.sci4.rx and e.sci4.tx==[tx>>8,tx&255]
        expected=[['write',0xFFFFF020,1,128],['read',0xFFFFF022,1,control],
            ['write',0xFFFFF022,1,control&252],['write',0xFFFFF026,1,250],
            ['write',0xFFFFF021,1,2],['read',0xFFFFF022,1,control&252],
            ['write',0xFFFFF022,1,(control&8)|48],['read',0xFFFFF024,1,192],
            ['write',0xFFFFF024,1,128]]
        for sent,received in zip([tx>>8,tx&255],[a,b]):
            expected += [['write',0xFFFFF023,1,sent],['read',0xFFFFF024,1,192],
                ['write',0xFFFFF024,1,120],['read',0xFFFFF024,1,192],
                ['read',0xFFFFF025,1,received],['read',0xFFFFF024,1,192],
                ['write',0xFFFFF024,1,184]]
        expected += [['read',0xFFFFF022,1,(control&8)|48],['write',0xFFFFF022,1,control&8]]
        assert e.sci4.accesses==expected
        plir=pins&0x380
        assert e.accesses==[('read',0xFFFFF75C,plir,2),('write',0xFFFFF75C,plir|512,2),
            ('read',0xFFFFF74E,pins,2),('write',0xFFFFF74E,pins&~2048,2),
            ('read',0xFFFFF74E,pins&~2048,2),('write',0xFFFFF74E,pins|2048,2),
            ('read',0xFFFFF75C,plir|512,2),('write',0xFFFFF75C,plir&~512,2)]
        cases+=1
    rejected=0
    for address,size,writing in [(0xFFFFF025,1,True),(0xFFFFF024,2,False),
                                (0xFFFFF027,1,False),(0xFFFFF020,2,True)]:
        io=Serial4(0xC0,[])
        try:io.write(address,0,size) if writing else io.read(address,size)
        except ValueError:rejected+=1
        else:raise AssertionError('unsupported access accepted')
    io=Serial4(0xC0,[])
    try:io.read(0xFFFFF025,1)
    except ValueError:rejected+=1
    else:raise AssertionError('receive exhausted accepted')
    result=dict(status='PASS',scope=__doc__,whole_ram_exchange_cases=cases,
        rejected_accesses=rejected,limits='ConstantSSR C0 and suppliedtwoRDRbytes. No external serialpeer/timing/status transitions, physical pin or absolutebaud proof.')
    Path(__file__).with_name('control-sci4-exchange-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result)


if __name__=='__main__':main()
