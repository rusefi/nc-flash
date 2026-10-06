/* Ghidra analysis output; verify against original SH instructions. */

/* WARNING: Removing unreachable block (ram,0x0001433c) */
/* Reads16-bit register, compares selected bit to descriptor polarity. First four input descriptors
   use FFFFF778 bits2..5, polarity0. */

bool Input_CompareSampledBit(short *param_1,uint param_2,undefined2 param_3)

{
  uint uVar1;
  uint uVar2;
  
  uVar2 = (uint)*param_1;
  uVar1 = (*(code *)PTR_FUN_00014364)(param_2 & 0xff,param_2,param_3,uVar2);
  uVar1 = uVar1 & uVar2;
  uVar2 = (*(code *)PTR_FUN_00014364)();
  return (uVar1 & 0xffff) == (uVar2 & 0xffff);
}

