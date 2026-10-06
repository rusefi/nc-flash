/* Ghidra analysis output; verify against original SH instructions. */

/* Protected16-bit write ofR5 toaddressR4 twice. Original duplicate writes observed; no timer side
   effects simulated. */

undefined4 Output_WriteCounterTwice(undefined2 *param_1,undefined2 param_2)

{
  undefined4 uVar1;
  undefined4 local_10;
  undefined2 uStack_c;
  undefined2 *puStack_8;
  
  uStack_c = param_2;
  puStack_8 = param_1;
  (*(code *)PTR_FUN_000110a0)(&local_10,(int)DAT_0001109c);
  *puStack_8 = uStack_c;
  *puStack_8 = uStack_c;
  uVar1 = (*(code *)PTR_FUN_000110a4)(local_10);
  return uVar1;
}

