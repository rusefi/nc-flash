/* Ghidra analysis output; verify against original SH instructions. */

/* Original final4530C producer. Always loads class limits; signedpositive8080 builds constant
   curves, replaces selected pointers then tags rising-class slots; publishes9C12.580 direct
   cases,12 retained calls and56 full proposal/selection replays; tcu-class-thresholds.txt. */

void Selection_ApplyClassThresholds(void)

{
  byte bVar1;
  int iVar2;
  
  bVar1 = TransmissionStateClass;
  iVar2 = (int)(char)TransmissionStateClass;
  Selection_LoadClassThresholdValues();
  if ('\0' < (char)bVar1) {
    Selection_BuildClassLimitCurves();
    Selection_ReplaceClassCurveSlots(iVar2);
    Selection_TagClassIncreaseSlots((int)*(char *)(int)DAT_00047300,iVar2);
  }
  *(byte *)(int)DAT_00047300 = bVar1;
  return;
}

