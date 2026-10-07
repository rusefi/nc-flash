"""Independent register, RAM-fill and original100D8 completion checks."""
import hashlib
import itertools
import json
from pathlib import Path
from sh_control_initialize_dma import RamFillStartup, DMAOR, SAR, DAR, COUNT, CONTROL
from verify_control_contributions import ECU
from verify_control_raw_inputs import application, expected_write


def configure(e, source, destination, count):
    e.write(DMAOR,1,2);e.write(SAR,source,4);e.write(DAR,destination,4)
    e.write(COUNT,count,4);e.write(CONTROL,0x1F0128,4)


def main():
    relative_calls=[]
    for pc in range(0,len(ECU)-1,2):
        opcode=int.from_bytes(ECU[pc:pc+2],'big')
        displacement=opcode&4095
        if displacement&2048:displacement-=4096
        if opcode>>12 in (10,11) and pc+4+2*displacement==0x100D8:
            relative_calls.append(dict(pc=pc,opcode=opcode,kind='BSR' if opcode>>12==11 else 'BRA'))
    assert dict(pc=0x100A2,opcode=0xB019,kind='BSR') in relative_calls
    halfwords = fills = rejected = flags = gates = 0
    for base in [SAR,DAR,COUNT,CONTROL]:
        for value in ([0,1,0x12345678,0xFFFFFFFF] if base in [SAR,DAR] else [0,1,0x123456,0xFFFFFF] if base==COUNT else [0,0x128,0x1F0128,0x1F3328]):
            e=RamFillStartup();e.dma_progress=False
            e.write(base,value>>16,2);e.write(base+2,value&65535,2)
            assert e.read(base,4)==value
            assert e.read(base,2)==value//65536 and e.read(base+2,2)==value%65536
            e.write(base,0,2);assert e.read(base,4)==value%65536
            halfwords+=1
    for base,mask in [(CONTROL,2),(DMAOR,2),(DMAOR,4),(DMAOR,6)]:
        e=RamFillStartup();e.dma[base]=mask
        try:e.write(base,0,2 if base==DMAOR else 4)
        except ValueError:pass
        else:raise AssertionError('Cleared unobserved DMA status')
        if base==CONTROL:
            e.read(base,2)
            try:e.write(base,0,4)
            except ValueError:pass
            else:raise AssertionError('High-half read incorrectly observed TE')
        e.read(base,2 if base==DMAOR else 4);e.write(base,0,2 if base==DMAOR else 4)
        assert e.dma[base]==0;flags+=1
    for value in [0,0x12345678,0xFFFFFFFF]:
        for count in [1,2,3,7,256]:
            for overlap in [False,True]:
                e=RamFillStartup();source=0xFFFF4100;dest=source if overlap else 0xFFFF5000
                e.write(source,value,4)
                for i in range(count):
                    if dest+i*4!=source:e.write(dest+i*4,0xA55AA55A,4)
                want=application(e)
                for i in range(count):expected_write(want,dest-0xFFFF0000+i*4,value,4)
                configure(e,source,dest,count);e.write(CONTROL,0x1F0129,4)
                assert application(e)==want and e.dma[SAR]==source and e.dma[DAR]==dest+4*count
                assert e.dma[COUNT]==0 and e.dma[CONTROL]==0x1F012B and len(e.dma_transfers)==1
                e.read(CONTROL,4);e.write(CONTROL,0x1F0128,4)
                assert e.dma[CONTROL]==0x1F0128;fills+=1
    for master, enable, ended, address_error, nmi in itertools.product(range(2), repeat=5):
        e=RamFillStartup();e.write(0xFFFF4100,0x12345678,4)
        e.dma.update({DMAOR:master+address_error*4+nmi*2,SAR:0xFFFF4100,DAR:0xFFFF5000,COUNT:1,CONTROL:0x1F0128+enable+ended*2})
        e._service()
        admitted=bool(master and enable and not ended and not address_error and not nmi)
        assert bool(e.dma_transfers)==admitted
        assert e.read(0xFFFF5000,4)==(0x12345678 if admitted else 0)
        gates+=1
    for address,size in [(DMAOR,1),(DMAOR,4),(SAR,1),(SAR+1,2),(SAR+2,4),(CONTROL+1,1),(DMAOR+2,2)]:
        for write in [False,True]:
            e=RamFillStartup()
            try:e.write(address,0,size) if write else e.read(address,size)
            except ValueError:rejected+=1
            else:raise AssertionError('Invalid register access admitted')
    for base,value,size in [(DMAOR,8,2),(COUNT,0x1000000,4),(CONTROL,0x10000000,4),(CONTROL,2,4),(DMAOR,6,2)]:
        e=RamFillStartup()
        try:e.write(base,value,size)
        except ValueError:rejected+=1
        else:raise AssertionError('Unsupported register write admitted')
    for source,dest,count,control in [(0xFFFF4100,0xFFFF5000,0,0x1F0129),
        (0xFFFF4100,0xFFFF5000,8193,0x1F0129),(0xFFFF4101,0xFFFF5000,1,0x1F0129),
        (0xFFFF4100,0xFFFFBFFC,2,0x1F0129),(0xFFFF4100,0xFFFF5000,1,0x1F1129)]:
        e=RamFillStartup();configure(e,source,dest,count)
        try:e.write(CONTROL,control,4)
        except NotImplementedError:rejected+=1
        else:raise AssertionError('Unsupported DMA transfer admitted')
        assert not e.dma_transfers
    routine=[]
    for seed in range(8):
        e=RamFillStartup()
        for address in range(0xFFFF3FFC,0xFFFFBFA4):e.write(address,((address*37+seed*19)%255)+1,1)
        want=application(e)
        for address in range(0x4000,0xBFA0):expected_write(want,address,0,1)
        before=e.r[8:16].copy();sr=e.sr;gbr=e.gbr
        e.run(0x100D8)
        assert application(e)==want and e.r[8:16]==before and e.sr==sr and e.gbr==gbr
        assert e.dma_transfers==[dict(source=0xFFFF4000,destination=0xFFFF4000,count=8168,final_destination=0xFFFFBFA0,final_count=0)]
        assert e.dma=={DMAOR:1,SAR:0xFFFF4000,DAR:0xFFFFBFA0,COUNT:0,CONTROL:0x1F0128}
        routine.append(dict(seed=seed,transfer=e.dma_transfers[0],accesses=e.accesses))
    e=RamFillStartup();e.dma_progress=False;e.write(0xFFFF9158,0xA55A,2)
    try:e.run(0x100D8,limit=2000)
    except RuntimeError as exc:withheld=str(exc)
    else:raise AssertionError('Firmware returned without DMA completion')
    assert not e.dma_transfers and e.read(0xFFFF9158,2)==0xA55A and e.dma[COUNT]==8168
    report=dict(rom_sha256=hashlib.sha256(ECU).hexdigest(),scope=__doc__,halfword_cases=halfwords,
                aligned_relative_caller_candidates=relative_calls,
                status_flag_cases=flags,admission_cases=gates,ram_fill_cases=fills,expected_rejections=rejected,
                original_routine_cases=routine,withheld_service=dict(status=withheld,pc=e.pc,tail=e.tail))
    Path(__file__).with_name('control-initialize-dma-verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS',halfwords,'register cases,',flags,'status cases,',gates,'gates,',fills,'fills,',rejected,'rejections,',len(routine),'original wholeRAM clears; withheld DMA stays waiting')


if __name__=='__main__':main()
