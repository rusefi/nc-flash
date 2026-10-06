/* Ghidra analysis output; verify against original SH instructions. */

/* Reads wordFFFFE400 and tests lowbyte01 (GSRbit0).128 register combinations. */

bool HCAN_ReadBusOffStatus(void)

{
  uint uVar1;
  
  uVar1 = FUN_00019ab6((int)DAT_00019abe);
  return (uVar1 & 1) != 0;
}

