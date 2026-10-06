/* Ghidra analysis output; verify against original SH instructions. */

/* STATIC: stop/start bit3 ofFFFFF401; zeroFFFFF442,FFFFF454=0A00. Physical timer identity/rate
   unproved. */

void Task_StartApplicationTimerLead(void)

{
  byte *pbVar1;
  
  pbVar1 = (byte *)(int)DAT_00016b04;
  *pbVar1 = *pbVar1 & 0xf7;
  *(undefined2 *)(int)DAT_00016b06 = 0;
  *(undefined2 *)(int)DAT_00016b0a = DAT_00016b08;
  *pbVar1 = *pbVar1 | 8;
  return;
}

