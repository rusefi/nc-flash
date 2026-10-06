/* Ghidra analysis output; verify against original SH instructions. */

/* Protected6A28=(B8244==1); stock1 bypasses factor division in3F97C, but not its zero-factor
   fallback. */

void CAN211_InitializeConversionBypass(void)

{
  if (*PTR_DAT_00034bf8 == '\x01') {
    (*(code *)PTR_FUN_00034c00)(PTR_CAN211_ConversionBypass_00034bfc,1);
    return;
  }
  (*(code *)PTR_FUN_00034c00)(PTR_CAN211_ConversionBypass_00034bfc,0);
  return;
}

