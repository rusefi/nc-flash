/* Ghidra analysis output; verify against original SH instructions. */

/* Release predicate independent of timer; normalclear/gate andalternate92D5bit7 with92C5bit2clear.
   Executed tcu-release-thresholds.txt. */

undefined4 Selection_ReleaseThresholdOverlay(void)

{
  bool bVar1;
  bool bVar2;
  char cVar3;
  undefined4 uVar4;
  
  bVar1 = ((int)(char)*PTR_ApplicationFaultFlags92D5_00045e58 & 0x80U) == 0;
  bVar2 = (*PTR_DAT_00045e5c & 0x40) == 0;
  cVar3 = (*(code *)PTR_Selection_AlternateOverlayRelease_00045e6c)();
  uVar4 = 0;
  if (((((bVar1) && (bVar2)) && ((*PTR_DAT_00045e68 & 4) == 0)) &&
      ((*PTR_ApplicationFaultFlags92D5_00045e58 & 1) == 0)) ||
     ((((bVar1 && (bVar2)) && (*PTR_Comparison_CompressedCategory_00045e60 != '\0')) ||
      (cVar3 == '\x01')))) {
    uVar4 = 1;
  }
  return uVar4;
}

