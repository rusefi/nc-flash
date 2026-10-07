"""Independent original4ACC configuration/wait/copy with finite ADC statuses."""
import hashlib,itertools,json,random
from pathlib import Path
from probe_control_scheduler_adc import SchedulerAdc,POLL
from verify_control_acquisition import REGISTERS
from verify_control_contributions import ECU,r,w
from verify_control_raw_inputs import application,expected_write
from verify_control_event2_activation import difference


def main():
    count=0
    for seed,delay in itertools.product(range(32),[0,1,3]):
        e=SchedulerAdc();rng=random.Random(seed);e.r[15]=0xFFFED000;e.sr=0xF0
        for a in range(0x4000,0x4060):w(e,a,rng.randrange(256))
        for a in e.adc_control:e.adc_control[a]=rng.randrange(256)
        for a in e.adc_samples:e.adc_samples[a]=rng.randrange(65536)
        e.poll_samples={a:[v]*delay+[v|128] for a,v in POLL.values()}
        memory=application(e);control=e.adc_control.copy();saved=e.r[8:16].copy();gbr=e.gbr
        expected_polls=[]
        for pc,(a,v) in POLL.items():
            expected_polls.extend([[pc,a,x] for x in [v]*delay+[v|128]])
            control[a]=v;control[a+1]=(control[a+1]&15)|32
        for i,a in enumerate(REGISTERS):expected_write(memory,0x4008+2*i,e.adc_samples[a],2)
        for a,v in [(0x404B,0),(0x404C,255),(0x404E,0),(0x4051,0),(0x4054,0)]:expected_write(memory,a,v,1)
        e.run(0x4ACC,limit=20000)
        assert application(e)==memory,(seed,delay,difference(e,memory))
        assert e.adc_control==control and e.poll_accesses==expected_polls and not any(e.poll_samples.values())
        assert e.adc_reads==REGISTERS and e.r[8:16]==saved and e.gbr==gbr and e.sr&0xF0==0xF0
        count+=1
    result=dict(status='PASS',scope=__doc__,rom_sha256=hashlib.sha256(ECU).hexdigest(),
        original_cases=count,explicit_nonready_polls=[0,1,3],result_words=32,
        limits='Finite supplied ADFflag/resultwords, not actualconversion/clock/IRQ. SRnonzero avoidsinlinepreemption.')
    Path(__file__).with_name('control-startup-adc-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result)


if __name__=='__main__':main()
