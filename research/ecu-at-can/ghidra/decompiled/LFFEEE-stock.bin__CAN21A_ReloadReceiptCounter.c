/* Ghidra analysis output; verify against original SH instructions. */

/* Writes6AB4 from ROM B8247=20. */

void CAN21A_ReloadReceiptCounter(void)

{
  *PTR_CAN21A_ReceiptCounter_00035784 = *PTR_DAT_00035780;
  return;
}

