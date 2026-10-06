/* Ghidra analysis output; verify against original SH instructions. */

/* Returns1 if88B4==1 or88B6==1. Strong P/N candidate; physical pin mapping unresolved. */

undefined4 Selector_CombineInputsZeroAndTwo(void)

{
  undefined4 uVar1;
  
  uVar1 = 0;
  if ((*PTR_Selector_FilteredInputTwo_00022cc0 == '\x01') ||
     (*PTR_Selector_FilteredInputZero_00022cc4 == '\x01')) {
    uVar1 = 1;
  }
  return uVar1;
}

