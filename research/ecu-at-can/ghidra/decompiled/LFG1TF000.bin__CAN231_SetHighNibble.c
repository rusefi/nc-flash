/* Ghidra analysis output; verify against original SH instructions. */

/* Payload byte0 upper nibble. */

undefined4 CAN231_SetHighNibble(void)

{
  undefined4 uVar1;
  
  uVar1 = (*(code *)PTR_Pack_MsbRelativeBitfield_0001c358)();
  return uVar1;
}

