/* Ghidra analysis output; verify against original SH instructions. */

/* 128 Boolean cases: exactly one among88B4/B5/B6/B7/BA/BB/BC, with singletonB7/BA/BB/BC. */

undefined4 SpeedFault_CheckSingletonInput(void)

{
  undefined4 uVar1;
  
  uVar1 = 0;
  if (((char)(*PTR_Selector_FilteredInputZero_000588c8 + *PTR_DAT_000588cc +
              *PTR_Selector_FilteredInputTwo_000588d0 + *PTR_DAT_000588b8 + *PTR_DAT_000588bc +
              *PTR_DAT_000588c0 + *PTR_DAT_000588c4) == '\x01') &&
     ((((*PTR_DAT_000588b8 == '\x01' || (*PTR_DAT_000588bc == '\x01')) ||
       (*PTR_DAT_000588c0 == '\x01')) || (*PTR_DAT_000588c4 == '\x01')))) {
    uVar1 = 1;
  }
  return uVar1;
}

