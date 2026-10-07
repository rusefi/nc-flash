/* Ghidra analysis output; verify against original SH instructions. */

/* Returns1 iff92D5bit7 set and92C5bit2clear. Executed alternate release. */

undefined4 Selection_AlternateOverlayRelease(void)

{
  undefined4 uVar1;
  
  uVar1 = 0;
  if ((((int)*DAT_000461f8 & 0x80U) != 0) && ((*PTR_DAT_000461fc & 4) == 0)) {
    uVar1 = 1;
  }
  return uVar1;
}

