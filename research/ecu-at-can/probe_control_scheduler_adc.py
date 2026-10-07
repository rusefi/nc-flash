"""Original scheduler/task17 startup with finite external ADC status/results.

Poll statuses are explicitly supplied at original4B62/4B6C/4B76. This is not
conversion timing, analog hardware or ADC interrupt delivery. No RAM flag injected.
"""
import json
from pathlib import Path
from probe_control_scheduler_cmt import SchedulerCmt
from probe_control_scheduler_start import main as sequence

POLL={0x4B62:(0xFFFFF818,0x33),0x4B6C:(0xFFFFF838,0x33),0x4B76:(0xFFFFF858,0x2B)}


class SchedulerAdc(SchedulerCmt):
    def __init__(self):
        super().__init__();self.poll_samples={a:[v,v|128] for a,v in POLL.values()};self.poll_accesses=[]
    def read(self,address,size):
        address &= 0xFFFFFFFF
        if self.pc in POLL and address==POLL[self.pc][0]:
            if size!=1 or not self.poll_samples[address]:raise ValueError('startup ADC finite byte sample exhausted')
            value=self.poll_samples[address].pop(0)
            self.poll_accesses.append([self.pc,address,value]);return value
        return super().read(address,size)


def main():
    e,result=sequence('control-scheduler-adc-probe.json',SchedulerAdc)
    result.update(adc_scope=__doc__,adc_poll_samples=e.poll_accesses,
        adc_remaining={hex(a):v for a,v in e.poll_samples.items()},
        adc_result_reads=e.adc_reads,cmt1_accesses=e.cmt1.accesses)
    Path(__file__).with_name('control-scheduler-adc-probe.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':main()
