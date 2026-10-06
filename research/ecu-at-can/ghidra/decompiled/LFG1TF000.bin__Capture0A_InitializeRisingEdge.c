/* Ghidra analysis output; verify against original SH instructions. */

/* Sets TIOR0 bits1:0=01, TIER0 bit0 and TSTR1 bit0;256 register-fixture executions. SH7055S manual
   identifies rising-edge input capture, not physical sensor wiring. */

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

