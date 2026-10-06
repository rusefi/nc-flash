/* Ghidra analysis output; verify against original SH instructions. */

/* BE payload bytes0-1. */

void CAN216_SetWord0(void)

{
  (*(code *)PTR_FUN_0001c60c)();
  (*(code *)PTR_Pack_MsbRelativeBitfield_0001c608)(PTR_CAN216_TxBuffer_0001c620);
  (*(code *)PTR_Pack_MsbRelativeBitfield_0001c608)();
  (*(code *)PTR_FUN_0001c614)();
  return;
}

