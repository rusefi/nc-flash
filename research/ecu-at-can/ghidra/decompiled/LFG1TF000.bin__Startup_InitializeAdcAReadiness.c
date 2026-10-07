/* Ghidra analysis output; verify against original SH instructions. */

/* 256 wholeRAM cases PASS:84A0=1,84A2word0,84A8/84AC/84B0long0; otherRAMpreserved.
   Originalinitialized low/recovery chain through112E6, no forcedreadyflags. tcu-readiness-a.txt. */

void Startup_InitializeAdcAReadiness(void)

{
  undefined4 *puVar1;
  undefined4 *puVar2;
  
  puVar1 = (undefined4 *)(int)DAT_0001139e;
  *PTR_Startup_AdcAReadinessState_000113ac = 1;
  puVar2 = (undefined4 *)(int)DAT_000113a0;
  *(undefined2 *)(int)DAT_0001139c = 0;
  *puVar1 = 0;
  *puVar2 = 0;
  *(undefined4 *)(int)DAT_000113a2 = 0;
  return;
}

