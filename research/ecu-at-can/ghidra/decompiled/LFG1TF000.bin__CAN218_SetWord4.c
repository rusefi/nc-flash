/* Ghidra analysis output; verify against original SH instructions. */

/* BE payload bytes4-5. */

void CAN218_SetWord4(void)

{
  (*(code *)PTR_FUN_0001c60c)();
  (*(code *)PTR_Pack_MsbRelativeBitfield_0001c608)(PTR_CAN218_TxBuffer_0001c610);
  (*(code *)PTR_Pack_MsbRelativeBitfield_0001c608)();
  (*(code *)PTR_FUN_0001c614)();
  return;
}

