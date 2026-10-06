/* Ghidra analysis output; verify against original SH instructions. */

/* Reconstructs ECU payload word0; paired machine-code verification. */

undefined2 CAN201_GetWord0(void)

{
  undefined2 uVar1;
  
  (*(code *)PTR_FUN_0001c8bc)();
  uVar1 = *(undefined2 *)PTR_CAN201_RxBuffer_0001c8cc;
  (*(code *)PTR_FUN_0001c8c4)();
  return uVar1;
}

