"""Bounded SH-2E RTE for original task dispatch with a NOP delay slot.

Renesas REJ09B0316-0200 section7.2.48: pop PC/SR, mask SR0FFF0FFF,
advance SP8, execute delay slot. Only aligned RAM frames, ROM destinations,
and NOP slots supported. No interrupt generation, exception handlers or time.
"""
from probe_control_acquisition_task import AcquisitionTask


class TaskDispatch(AcquisitionTask):
    def __init__(self):
        super().__init__();self.rte_transfers=[]
    def instruction(self,pc):
        if self.read(pc,2)!=0x002B:
            return super().instruction(pc)
        sp=self.r[15]
        if sp&3 or not 0xFFFE0000<=sp<=0xFFFFBFF8:
            raise ValueError('RTE fixture requires aligned mapped RAM frame')
        target=self.read(sp,4);status=self.read(sp+4,4)
        if target&1 or not 0<=target<len(self.rom):
            raise ValueError('RTE fixture requires aligned ROM destination')
        if self.read(pc+2,2)!=0x0009:
            raise NotImplementedError('RTE fixture supports only NOP delay slot')
        self.sr=status&0x0FFF0FFF;self.r[15]=sp+8;self.visited.add(pc)
        self.rte_transfers.append(dict(pc=pc,sp=sp,target=target,status=status,restored_sr=self.sr))
        return target,True
