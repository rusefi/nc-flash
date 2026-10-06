/* Ghidra analysis output; verify against original SH instructions. */

/* All256 bit0 combinations tested; requiresA959/A95A/A95B/A95C/A95D/A95E/A960/A961. A95F excluded.
    */

undefined4 SpeedFault_CheckDiagnosticPrerequisites(void)

{
  undefined4 uVar1;
  
  uVar1 = 0;
  if ((((((PTR_DAT_000588d4[1] & 1) == 1) && ((PTR_DAT_000588d4[2] & 1) == 1)) &&
       ((PTR_DAT_000588d4[3] & 1) == 1)) &&
      (((PTR_DAT_000588d4[4] & 1) == 1 && ((PTR_DAT_000588d4[5] & 1) == 1)))) &&
     (((PTR_DAT_000588d4[6] & 1) == 1 &&
      (((PTR_DAT_000588d4[8] & 1) == 1 && ((PTR_DAT_000588d4[9] & 1) == 1)))))) {
    uVar1 = 1;
  }
  return uVar1;
}

