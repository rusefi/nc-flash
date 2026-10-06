/* Ghidra analysis output; verify against original SH instructions. */

/* Copies calibrationB8248=20 into6B04. */

void CAN4B0_ReloadReceiptCounter(void)

{
  *PTR_DAT_00036020 = *PTR_DAT_0003601c;
  return;
}

