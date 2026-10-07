/* Ghidra analysis output; verify against original SH instructions. */

/* Returns1 iff92D5bit7 and92C5bit2. Executed alternate entry; no physicalsignalclaim. */

undefined4 Selection_AlternateOverlayEntry(void)

{
  undefined4 uVar1;
  
  uVar1 = 0;
  if ((((int)*DAT_000461f8 & 0x80U) != 0) && ((*PTR_DAT_000461fc & 4) != 0)) {
    uVar1 = 1;
  }
  return uVar1;
}

