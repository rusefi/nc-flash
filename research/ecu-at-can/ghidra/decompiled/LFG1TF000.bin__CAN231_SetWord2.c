/* Ghidra analysis output; verify against original SH instructions. */

/* BE payload bytes2-3. */

void CAN231_SetWord2(void)

{
  (*(code *)PTR_FUN_0001c4ac)();
  (*(code *)PTR_Pack_MsbRelativeBitfield_0001c4a8)(PTR_CAN231_TxBuffer_0001c4b0);
  (*(code *)PTR_Pack_MsbRelativeBitfield_0001c4a8)();
  (*(code *)PTR_FUN_0001c4b4)();
  return;
}

