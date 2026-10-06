/* Ghidra analysis output; verify against original SH instructions. */

/* Sets6A38 and6A3C float1. No payload writer established; do not call these CAN216 fields. */

void AT_InitializeConversionInputs(void)

{
  *(undefined4 *)PTR_DAT_000350b8 = 0x3f800000;
  *DAT_000350bc = 0x3f800000;
  return;
}

