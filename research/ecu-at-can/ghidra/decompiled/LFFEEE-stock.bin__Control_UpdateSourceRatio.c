/* Ghidra analysis output; verify against original SH instructions. */

/* 802C nearzero clears8028;else both8038/803C outsideindividualeps
   computesRTZ(802C/RTZ(8038*803C));elsehold. Alwayscalls5AACC/5AAF0 status producers.343 cases
   andretainedserialhistory; control-history.txt. */

void Control_UpdateSourceRatio(void)

{
  undefined *puVar1;
  char cVar2;
  char cVar3;
  char cVar4;
  float fVar5;
  float fVar6;
  float fVar7;
  undefined4 uVar8;
  
  puVar1 = PTR_FUN_00058560;
  uVar8 = 0;
  fVar7 = *(float *)PTR_Control_SelectedRatioNumerator_0005855c;
  cVar2 = (*(code *)PTR_FUN_00058560)(fVar7,0,DAT_00058564);
  fVar5 = *(float *)PTR_Control_RatioMapFactor_00058568;
  cVar3 = (*(code *)puVar1)(fVar5,uVar8,DAT_0005856c);
  fVar6 = *(float *)PTR_Control_RatioEnvironmentFactor_00058570;
  cVar4 = (*(code *)puVar1)(fVar6,uVar8,DAT_00058574);
  if (cVar2 == '\0') {
    *(undefined4 *)PTR_Control_RetainedSourceRatio_00058578 = uVar8;
  }
  else if ((cVar3 != '\0') && (cVar4 != '\0')) {
    *(float *)PTR_Control_RetainedSourceRatio_00058578 = fVar7 / (fVar5 * fVar6);
  }
  (*(code *)PTR_Control_UpdateSourceDeltaHigh_0005857c)();
                    /* WARNING: Could not recover jumptable at 0x000583b4. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*(code *)PTR_Control_UpdateSourceDeltaNonpositive_00058580)();
  return;
}

