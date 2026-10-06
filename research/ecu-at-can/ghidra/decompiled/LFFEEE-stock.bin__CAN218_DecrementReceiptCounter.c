/* Ghidra analysis output; verify against original SH instructions. */

/* Counter FFFF6A90; B824A reload under network/reset states. */

void CAN218_DecrementReceiptCounter(void)

{
  undefined4 uVar1;
  
  uVar1 = (*(code *)PTR_FUN_00035200)(0x10);
  if ((*PTR_DAT_00035208 == '\0') && (((int)(char)*PTR_DAT_0003520c & 0x80U) == 0)) {
    if (*PTR_CAN218_ReceiptCounter_00035204 != '\0') {
      *PTR_CAN218_ReceiptCounter_00035204 = *PTR_CAN218_ReceiptCounter_00035204 + (char)DAT_000351e4
      ;
    }
  }
  else {
    *PTR_CAN218_ReceiptCounter_00035204 = *PTR_DAT_00035210;
  }
  (*(code *)PTR_FUN_00035214)(uVar1);
  return;
}

