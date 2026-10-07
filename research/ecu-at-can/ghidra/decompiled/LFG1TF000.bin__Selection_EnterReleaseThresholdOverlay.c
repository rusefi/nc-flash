/* Ghidra analysis output; verify against original SH instructions. */

/* Normal92D5bit0 entry with fault/gate/6331 checks
   andpending/code0..4block;alternate92D5bit7+92C5bit2 bypassesnormal conditions.
   Doesnotbypass45CE4. */

undefined4 Selection_EnterReleaseThresholdOverlay(void)

{
  bool bVar1;
  short sVar2;
  char cVar3;
  char cVar4;
  char cVar5;
  undefined4 uVar6;
  
  sVar2 = DAT_ffff80ea;
  cVar3 = (*(code *)PTR_Phase_HasPendingWork_00045e4c)();
  cVar4 = (*(code *)PTR_Phase_ClassifyDirection_00045e50)((int)DAT_ffff8089);
  cVar5 = (*(code *)PTR_Selection_AlternateOverlayEntry_00045e54)();
  uVar6 = 0;
  bVar1 = false;
  if ((cVar3 != '\0') && (cVar4 == '\0')) {
    bVar1 = true;
  }
  if ((((((((int)(char)*PTR_ApplicationFaultFlags92D5_00045e58 & 0x80U) == 0) &&
         ((*PTR_DAT_00045e5c & 0x40) == 0)) && ((*PTR_ApplicationFaultFlags92D5_00045e58 & 1) == 1))
       && (*PTR_Comparison_CompressedCategory_00045e60 == '\0')) &&
      (((sVar2 < *(short *)PTR_DAT_00045e64 ||
        (((*PTR_DAT_00045e68 & 4) != 0 && (*(short *)PTR_DAT_00045e64 <= sVar2)))) && (!bVar1)))) ||
     (cVar5 == '\x01')) {
    uVar6 = 1;
  }
  return uVar6;
}

