/* Ghidra analysis output; verify against original SH instructions. */

/* 256 exactMMIO/unchangedRAM cases: F401stopbit3,F442zero,F4540A00,F401startbit3;
   allinitialstartbytes. CompatibleTCR1B4/PSCR1 suggestsPphi/32; nohardwarecounter/startoffset
   proof. tcu-application-interrupt.txt. */

void Task_InitializeApplicationTimer(void)

{
  byte *pbVar1;
  
  pbVar1 = (byte *)(int)DAT_00016b04;
  *pbVar1 = *pbVar1 & 0xf7;
  *(undefined2 *)(int)DAT_00016b06 = 0;
  *(undefined2 *)(int)DAT_00016b0a = DAT_00016b08;
  *pbVar1 = *pbVar1 | 8;
  return;
}

