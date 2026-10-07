/* Ghidra analysis output; verify against original SH instructions. */

/* Stock5678/567B=(536C>=6.5);5679=(722A1and56771);567A=(536C>=6.5and5680zero).
   StockcalibrationDCEbytes0. Originalbodyexecuted. */

undefined * Control_UpdateLocalSerialEnables(void)

{
  ushort uVar1;
  undefined *puVar2;
  byte bVar4;
  undefined *puVar3;
  undefined *puVar5;
  float fVar6;
  
  uVar1 = *(ushort *)PTR_Control_ModeOneTimer_00024f54;
  fVar6 = *(float *)PTR_Control_FilteredLocalSource_00024f44;
  bVar4 = (*(code *)PTR_FUN_00024f5c)(PTR_Control_FilteredModeInput_00024f58);
  puVar2 = PTR_DAT_00024f64;
  if ((fVar6 < *(float *)PTR_DAT_00024f64) ||
     (((*PTR_DAT_00024f68 != '\0' && ((bVar4 != 1 || (uVar1 < *(ushort *)PTR_DAT_00024f6c)))) ||
      (*PTR_DAT_00024f70 != '\0')))) {
    *PTR_DAT_00024f60 = 0;
  }
  else {
    *PTR_DAT_00024f60 = 1;
  }
  puVar5 = (undefined *)(uint)bVar4;
  puVar3 = puVar5;
  if ((((puVar5 == (undefined *)0x1) && (*(ushort *)PTR_DAT_00024f6c <= uVar1)) &&
      (puVar3 = (undefined *)(uint)(byte)*PTR_Control_QualifiedSerialFeedback_00024f24,
      puVar3 == (undefined *)0x1)) &&
     (puVar3 = (undefined *)(int)(char)*PTR_DAT_00024f74, puVar3 == (undefined *)0x0)) {
    *PTR_DAT_00024f78 = 1;
  }
  else {
    *PTR_DAT_00024f78 = 0;
  }
  if ((((fVar6 < *(float *)puVar2) ||
       (*(short *)PTR_Control_SerialMonitorHoldoffCounter_00024f3c != 0)) ||
      ((puVar3 = (undefined *)0x0, *PTR_DAT_00024f80 != '\0' &&
       ((puVar3 = puVar5, puVar5 != (undefined *)0x1 ||
        (puVar3 = PTR_DAT_00024f6c, uVar1 < *(ushort *)PTR_DAT_00024f6c)))))) ||
     (*PTR_DAT_00024f84 != '\0')) {
    *PTR_Control_LocalMissingFeedbackEnable_00024f7c = 0;
  }
  else {
    *PTR_Control_LocalMissingFeedbackEnable_00024f7c = 1;
  }
  if ((fVar6 < *(float *)puVar2) || (*PTR_DAT_00024f70 != '\0')) {
    *PTR_DAT_00024f88 = 0;
  }
  else {
    *PTR_DAT_00024f88 = 1;
  }
  return puVar3;
}

