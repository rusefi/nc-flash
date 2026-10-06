/* Ghidra analysis output; verify against original SH instructions. */

/* TestsGSR atFFFFE401 bit0 ->1AC7A; writes6000 toIRR FFFFE412.128 original-code body tests stop
   beforeRTE1B422; no interrupt/electrical timing model. */

undefined8 HCAN_ErrorHandler(void)

{
  undefined4 in_r0;
  undefined4 in_r1;
  
  if ((*(byte *)(int)DAT_0001b4f4 & 1) != 0) {
    (*(code *)PTR_HCAN_LatchBusOffRecovery_0001b504)();
  }
  *(undefined2 *)(int)DAT_0001b4f8 = DAT_0001b4f6;
  return CONCAT44(in_r1,in_r0);
}

