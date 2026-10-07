/* Ghidra analysis output; verify against original SH instructions. */

/* Any8F30 forces68FC/67E4=66.25, retaining695C/6960/67E0. ElsemapA3804/33C02/33C2A
   then6D40+67E0+6960;stockDB0C1=0 directcopy.1275direct/36caller/80retained/320pairedcycles;
   control-target-source.txt. */

void TargetInput_Produce(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined4 uVar5;
  float fVar6;
  
  puVar4 = PTR_DAT_00030f28;
  puVar3 = PTR_FUN_00030ee4;
  puVar2 = PTR_TargetInput_Produced_00030edc;
  puVar1 = PTR_TargetInput_Combined_00030ed8;
  if (*PTR_Control_RawSecondFallbackLatch_00030ee0 == '\0') {
    uVar5 = (*(code *)PTR_FUN_00030ee4)(PTR_SpeedCandidate_ProtectedSelected_00030ee8);
    uVar5 = (*(code *)PTR_Lookup_FloatCurve_00030ef0)(uVar5,PTR_PTR_00030eec);
    puVar4 = PTR_TargetInput_ExtraCorrection_00030ef8;
    *(undefined4 *)PTR_TargetInput_MappedCorrection_00030ef4 = uVar5;
    (*(code *)puVar4)();
    (*(code *)PTR_TargetInput_FilterCorrection_00030efc)();
    fVar6 = (float)(*(code *)puVar3)(PTR_Control_RawSecondPublished_00030f00);
    puVar4 = PTR_DAT_00030f0c;
    *(float *)puVar1 =
         fVar6 + *(float *)PTR_TargetInput_RetainedCorrection_00030f04 +
         *(float *)PTR_TargetInput_ExtraTerm_00030f08;
    if (((*puVar4 != '\x01') ||
        (fVar6 = (float)(*(code *)puVar3)(PTR_Control_RawFirstPublished_00030f10),
        fVar6 <= *(float *)PTR_DAT_00030f14)) || (*(short *)PTR_DAT_00030f18 != 0)) {
      *(undefined4 *)puVar2 = *(undefined4 *)puVar1;
    }
    else {
      uVar5 = (*(code *)PTR_FUN_00030f24)
                        (*(undefined4 *)puVar1,*(undefined4 *)puVar2,
                         1.0 - *(float *)PTR_DAT_00030f1c,DAT_00030f20);
      *(undefined4 *)puVar2 = uVar5;
    }
  }
  else {
    *(undefined4 *)PTR_TargetInput_Combined_00030ed8 = *(undefined4 *)PTR_DAT_00030f28;
    *(undefined4 *)puVar2 = *(undefined4 *)puVar4;
  }
  return;
}

