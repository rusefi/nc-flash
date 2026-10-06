/* Ghidra analysis output; verify against original SH instructions. */

/* Payload byte6. */

undefined4 CAN218_SetByte6(void)

{
  undefined4 uVar1;
  
  uVar1 = (*(code *)PTR_Pack_MsbRelativeBitfield_0001c608)();
  return uVar1;
}

