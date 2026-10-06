/* Ghidra analysis output; verify against original SH instructions. */

/* BE payload bytes0-1. */

void CAN218_SetWord0(void)

{
  (*(code *)PTR_FUN_0001c4ac)();
  (*(code *)PTR_Pack_MsbRelativeBitfield_0001c4a8)(PTR_CAN218_TxBuffer_0001c4c8);
  (*(code *)PTR_Pack_MsbRelativeBitfield_0001c4a8)();
  (*(code *)PTR_FUN_0001c4b4)();
  return;
}

