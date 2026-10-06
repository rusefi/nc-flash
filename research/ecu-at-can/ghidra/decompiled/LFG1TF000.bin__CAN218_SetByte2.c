/* Ghidra analysis output; verify against original SH instructions. */

/* Payload byte2. */

undefined4 CAN218_SetByte2(void)

{
  undefined4 uVar1;
  
  uVar1 = (*(code *)PTR_Pack_MsbRelativeBitfield_0001c4a8)();
  return uVar1;
}

