/* Ghidra analysis output; verify against original SH instructions. */

/* Original software double helpers yield s32-saturate(a*b/2^shift), truncating toward zero.175
   signed/saturation cases for shifts0/1/8/16/31. Used in212F4 history normalization. See
   tcu-measurement.txt. */

undefined4 Arithmetic_SaturatingMultiplyShift(void)

{
  undefined4 uVar1;
  undefined1 *local_3c [3];
  undefined1 *local_30;
  undefined1 *local_2c [3];
  undefined1 *local_20;
  undefined1 auStack_1c [28];
  
  (*(code *)PTR_FUN_00010d24)();
  local_20 = (undefined1 *)&local_20;
  (*(code *)PTR_FUN_00010d2c)();
  local_2c[0] = (undefined1 *)local_2c;
  (*(code *)PTR_FUN_00010d2c)();
  local_30 = auStack_1c;
  (*(code *)PTR_FUN_00010d30)();
  local_3c[0] = (undefined1 *)local_3c;
  (*(code *)PTR_FUN_00010d34)();
  (*(code *)PTR_FUN_00010d38)();
  (*(code *)PTR_FUN_00010d44)();
  (*(code *)PTR_FUN_00010d4c)();
  uVar1 = (*DAT_00010d50)();
  return uVar1;
}

