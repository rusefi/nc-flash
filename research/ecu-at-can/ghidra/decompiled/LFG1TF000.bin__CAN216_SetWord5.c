/* Ghidra analysis output; verify against original SH instructions. */

/* BE payload bytes5-6. */

void CAN216_SetWord5(void)

{
  (*(code *)PTR_FUN_0001c774)();
  (*(code *)PTR_Pack_MsbRelativeBitfield_0001c77c)(PTR_CAN216_TxBuffer_0001c778);
  (*(code *)PTR_Pack_MsbRelativeBitfield_0001c77c)();
  (*(code *)PTR_FUN_0001c780)();
  return;
}

