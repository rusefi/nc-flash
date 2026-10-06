/* Ghidra analysis output; verify against original SH instructions. */

/* Reads word atFFFFE400; tests0200 (MCRbit1 in high byte), NOT a GSR bit.128 register combinations.
    */

bool HCAN_ReadHaltRequest(void)

{
  ushort uVar1;
  
  uVar1 = FUN_00019ab6((int)DAT_00019abe);
  return (DAT_00019ac4 & uVar1) != 0;
}

