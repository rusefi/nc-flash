/* Ghidra analysis output; verify against original SH instructions. */

/* 256originalwholeRAM/exact8MMIOcases PASS:TIOR0bit0set/bit1clear,TIER0bit0set,TSTR1bit0set.
   CompatibleSH7055S risingedgeICR0A onsharedTCNT0;PSCR1=1 impliesPphi/2,nosecondTCR0scale. No
   counterreset/physicalsensor/IRQadmission. tcu-capture-clock.txt. */

void Capture0A_InitializeRisingEdge(void)

{
  byte *pbVar1;
  
  pbVar1 = (byte *)(int)DAT_00016cce;
  *pbVar1 = *pbVar1 | 1;
  *pbVar1 = *pbVar1 & 0xfd;
  *(ushort *)(pbVar1 + 4) = *(ushort *)(pbVar1 + 4) | 1;
  pbVar1[-0x29] = pbVar1[-0x29] | 1;
  return;
}

