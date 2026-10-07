/* Ghidra analysis output; verify against original SH instructions. */

/* Unsigned comparison of signed byte loads821E and7714C=61. Called by state1 even when36BDA
   rejected; rejected admission already clears821E. Standalone all-byte timer semantics not
   independently tested. */

bool ClassAdjustment_TimerAdmission(void)

{
  return (byte)*PTR_DAT_00036e48 <= (byte)*PTR_DAT_00036e44;
}

