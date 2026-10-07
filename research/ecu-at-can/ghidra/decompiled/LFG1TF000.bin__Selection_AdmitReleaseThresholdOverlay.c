/* Ghidra analysis output; verify against original SH instructions. */

/* RequiresclassnotFF/0/1,signed80EA>=256,9330bit0clear,sourcenot11..14. Original executed;
   tcu-release-thresholds.txt. */

undefined4 Selection_AdmitReleaseThresholdOverlay(void)

{
  char cVar1;
  undefined4 uVar2;
  
  cVar1 = *PTR_Selection_SourceCode_00045e40;
  uVar2 = 0;
  if ((((((TransmissionStateClass != 0xff) && (TransmissionStateClass != 0)) &&
        (TransmissionStateClass != 1)) &&
       ((*(short *)PTR_DAT_00045e44 <= DAT_ffff80ea && ((*PTR_DAT_00045e48 & 1) == 0)))) &&
      ((cVar1 != '\v' && ((cVar1 != '\f' && (cVar1 != '\r')))))) && (cVar1 != '\x0e')) {
    uVar2 = 1;
  }
  return uVar2;
}

