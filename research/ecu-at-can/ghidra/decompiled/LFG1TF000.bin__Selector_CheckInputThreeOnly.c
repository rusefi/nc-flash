/* Ghidra analysis output; verify against original SH instructions. */

/* Requires 88B7==1 and 88B4/B5/B6/BA/BC zero. Executes immediate active recovery for groups15/16
   via58548 and5662A; physical position remains unproven. */

undefined4 Selector_CheckInputThreeOnly(void)

{
  undefined4 uVar1;
  
  uVar1 = 0;
  if ((((*PTR_Selector_FilteredInputZero_000586d4 == '\0') && (*PTR_DAT_000586d8 == '\0')) &&
      (*PTR_Selector_FilteredInputTwo_000586dc == '\0')) &&
     (((*PTR_DAT_000586e0 == '\x01' && (*PTR_DAT_000586e4 == '\0')) && (*PTR_DAT_000586e8 == '\0')))
     ) {
    uVar1 = 1;
  }
  return uVar1;
}

