/* Ghidra analysis output; verify against original SH instructions. */

/* 256 original startups PASS,18 exactMMIO
   each:stopTSTR1bit4,clearTSR3bit0,enableTIER3bit0,TIOR3Alow1,TCNT3zero,GR3A15625,start.
   ExistingPSCR1=1/TCR3=4 implies500000phi compareperiod. No physicalclock/fullboot.
   tcu-diagnostic-timer.txt. */

void DiagnosticTimer_InitializeCompare(void)

{
  ushort *puVar1;
  byte *pbVar2;
  byte *pbVar3;
  
  pbVar3 = (byte *)(int)DAT_00016890;
  *pbVar3 = *pbVar3 & 0xef;
  puVar1 = (ushort *)(int)DAT_00016892;
  *puVar1 = *puVar1 & (ushort)PTR_DAT_0001689c;
  puVar1[1] = puVar1[1] | 1;
  pbVar2 = (byte *)((int)puVar1 + 0x2b);
  *pbVar2 = *pbVar2 & 0xf7;
  *pbVar2 = *pbVar2 & 0xfb;
  *pbVar2 = *pbVar2 & 0xfd;
  *pbVar2 = *pbVar2 | 1;
  *(undefined2 *)(int)DAT_00016894 = 0;
  *(undefined2 *)(int)DAT_00016898 = DAT_00016896;
  *pbVar3 = *pbVar3 | 0x10;
  return;
}

