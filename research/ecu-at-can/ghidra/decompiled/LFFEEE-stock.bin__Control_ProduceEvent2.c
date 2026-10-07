/* Ghidra analysis output; verify against original SH instructions. */

/* Reads535C/tests butunconditionallytails2BC8C withR4=2. Originalwrapperchain wholeRAM/admission
   and120queuedcycles PASS; no535Cgateclaim. control-queued-event2.txt. */

void Control_ProduceEvent2(void)

{
  (*(code *)PTR_Control_EnqueueLimitedEvent_000182ac)(2);
  return;
}

