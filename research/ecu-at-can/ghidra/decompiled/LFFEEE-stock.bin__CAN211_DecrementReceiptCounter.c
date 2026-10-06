/* Ghidra analysis output; verify against original SH instructions. */

/* Counter6A1E decrements with saturation;69E0>0 or735A bit80 reloads B8246=20. Call period
   unproven. */

void CAN211_DecrementReceiptCounter(void)

{
  undefined4 uVar1;
  
  uVar1 = (*(code *)PTR_FUN_00034a20)(0x10);
  if ((*PTR_DAT_00034a28 == '\0') && (((int)(char)*PTR_DAT_00034a2c & 0x80U) == 0)) {
    if (*PTR_DAT_00034a24 != '\0') {
      *PTR_DAT_00034a24 = *PTR_DAT_00034a24 + (char)DAT_00034a0c;
    }
  }
  else {
    *PTR_DAT_00034a24 = *PTR_DAT_00034a30;
  }
  (*(code *)PTR_FUN_00034a34)(uVar1);
  return;
}

