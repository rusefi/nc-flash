/* Ghidra analysis output; verify against original SH instructions. */

/* 256originalwholeRAM/exact8MMIOcases PASS:TIOR0bit2set/bit3clear,TIER0bit1set,TSTR1bit0set.
   ICR0Bshares32bitTCNT0 withA. CompatiblePSCR1=1 givesPphi/2; oldonce/app timestampincrements
   inconsistentwith81920phiappperiod. No physicalsensor/IRQproof. tcu-capture-clock.txt. */

void Capture0B_InitializeRisingEdge(void)

{
  byte *pbVar1;
  
  pbVar1 = (byte *)(int)DAT_00016b96;
  *pbVar1 = *pbVar1 | 4;
  *pbVar1 = *pbVar1 & 0xf7;
  *(ushort *)(pbVar1 + 4) = *(ushort *)(pbVar1 + 4) | 2;
  pbVar1[-0x29] = pbVar1[-0x29] | 1;
  return;
}

