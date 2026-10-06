/* Ghidra analysis output; verify against original SH instructions. */

/* Counter FFFF6AD8; B824B reload under network/reset states. */

void CAN231_DecrementReceiptCounter(void)

{
  undefined4 uVar1;
  
  uVar1 = (*(code *)PTR_FUN_00035844)(0x10);
  if ((*PTR_DAT_0003584c == '\0') && (((int)(char)*PTR_DAT_00035850 & 0x80U) == 0)) {
    if (*PTR_CAN231_ReceiptCounter_00035848 != '\0') {
      *PTR_CAN231_ReceiptCounter_00035848 = *PTR_CAN231_ReceiptCounter_00035848 + (char)DAT_0003582a
      ;
    }
  }
  else {
    *PTR_CAN231_ReceiptCounter_00035848 = *PTR_DAT_00035854;
  }
  (*(code *)PTR_FUN_00035858)(uVar1);
  return;
}

