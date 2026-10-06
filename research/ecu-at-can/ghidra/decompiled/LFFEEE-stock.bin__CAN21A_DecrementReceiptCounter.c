/* Ghidra analysis output; verify against original SH instructions. */

/* Executed6AB4 decrement saturating0, reset20 if69E0 nonzero or735A bit7.3880/3894 preserve
   interrupt mask only; optional scheduler tail gated in fixture. */

void CAN21A_DecrementReceiptCounter(void)

{
  undefined4 uVar1;
  
  uVar1 = (*(code *)PTR_FUN_00035704)(0x10);
  if ((*PTR_DAT_00035708 == '\0') && (((int)(char)*PTR_DAT_0003570c & 0x80U) == 0)) {
    if (*PTR_CAN21A_ReceiptCounter_000356c4 != '\0') {
      *PTR_CAN21A_ReceiptCounter_000356c4 = *PTR_CAN21A_ReceiptCounter_000356c4 + (char)DAT_0003576e
      ;
    }
  }
  else {
    *PTR_CAN21A_ReceiptCounter_000356c4 = *PTR_DAT_00035710;
  }
  (*(code *)PTR_FUN_00035770)(uVar1);
  return;
}

