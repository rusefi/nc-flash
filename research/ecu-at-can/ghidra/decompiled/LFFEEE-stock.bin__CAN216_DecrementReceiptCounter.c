/* Ghidra analysis output; verify against original SH instructions. */

/* Counter FFFF6A5D; B8249 reload under network/reset states. */

void CAN216_DecrementReceiptCounter(void)

{
  undefined4 uVar1;
  
  uVar1 = (*(code *)PTR_FUN_00034cd4)(0x10);
  if ((*PTR_DAT_00034cdc == '\0') && (((int)(char)*PTR_DAT_00034ce0 & 0x80U) == 0)) {
    if (*PTR_CAN216_ReceiptCounter_00034cd8 != '\0') {
      *PTR_CAN216_ReceiptCounter_00034cd8 = *PTR_CAN216_ReceiptCounter_00034cd8 + (char)DAT_00034cac
      ;
    }
  }
  else {
    *PTR_CAN216_ReceiptCounter_00034cd8 = *PTR_DAT_00034ce4;
  }
  (*(code *)PTR_FUN_00034ce8)(uVar1);
  return;
}

