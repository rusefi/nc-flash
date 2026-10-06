/* Ghidra analysis output; verify against original SH instructions. */

/* B8246 stock20 ->6A1E. Counter units unresolved. */

void CAN211_ReloadReceiptCounter(void)

{
  *DAT_00034bf4 = *PTR_DAT_00034bf0;
  return;
}

