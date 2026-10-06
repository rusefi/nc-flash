/* Ghidra analysis output; verify against original SH instructions. */

/* Executed:80B2=9240 andA53C=0. */

void CAN215_InitializeSecondApplicationValue(void)

{
  CAN215_SecondApplicationValue = *DAT_0005184c;
  *PTR_CAN215_SecondSelectionStatus_00051850 = 0;
  return;
}

