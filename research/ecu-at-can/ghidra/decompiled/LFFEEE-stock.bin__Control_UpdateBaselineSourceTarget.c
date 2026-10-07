/* Ghidra analysis output; verify against original SH instructions. */

/* 80A0 clears if7346==1 orA3A4==1 or both80A8/7012zero; other side outputs hold. Else mapA3628
   if734A bit40 or7EEE>0, otherwiseA363C, input6DB4/6CD4; stepped6D28 factor80B0/100. RTZ each op;
   control-baseline-source.txt. */

undefined4 * Control_UpdateBaselineSourceTarget(void)

{
  short sVar1;
  undefined *puVar2;
  undefined *puVar3;
  char cVar5;
  undefined4 *puVar4;
  undefined *puVar6;
  short sVar7;
  undefined4 uVar8;
  float fVar9;
  undefined4 uStack_10;
  
  puVar2 = PTR_FUN_00058c74;
  cVar5 = (*(code *)PTR_FUN_00058c74)(PTR_DAT_00058c7c);
  puVar4 = (undefined4 *)0x1;
  if (cVar5 != '\x01') {
    cVar5 = (*(code *)puVar2)(PTR_DAT_00058c80);
    puVar4 = (undefined4 *)0x1;
    if (cVar5 != '\x01') {
      if (*PTR_Control_BaselineSourceCountdown_00058c6c == '\0') {
        cVar5 = (*(code *)puVar2)(PTR_DAT_00058c84);
        puVar4 = (undefined4 *)0x0;
        if (cVar5 == '\0') goto LAB_00058c0c;
      }
      puVar3 = PTR_Control_BaselineSourceMappedValue_00058c8c;
      puVar2 = PTR_FUN_00058c54;
      if (((*PTR_TransmissionModeFlags_00058c90 & 0x40) == 0) &&
         (cVar5 = (*(code *)PTR_FUN_00058c74)(PTR_DAT_00058c94), cVar5 == '\0')) {
        uStack_10 = (*(code *)puVar2)(PTR_DAT_00058d90);
        uVar8 = (*(code *)puVar2)(PTR_DAT_00058d94);
        puVar6 = PTR_Control_BaselineTargetATDescriptor_00058d98;
      }
      else {
        uStack_10 = (*(code *)puVar2)(PTR_DAT_00058c98);
        uVar8 = (*(code *)puVar2)(PTR_DAT_00058c9c);
        puVar6 = PTR_Control_BaselineTargetMTOrExtraDescriptor_00058ca0;
      }
      uVar8 = (*(code *)PTR_Lookup_FloatMap2D_00058d9c)(uVar8,uStack_10,puVar6);
      puVar6 = PTR_Control_RawFirstAlternate_00058da0;
      *(undefined4 *)puVar3 = uVar8;
      fVar9 = (float)(*(code *)puVar2)(puVar6);
      puVar2 = PTR_Control_BaselineSourceFactorBin_00058da4;
      if (*(float *)PTR_DAT_00058da8 <= fVar9) {
        sVar1 = *(short *)PTR_Control_BaselineTargetFactorDescriptor_00058dac;
        if (fVar9 < *(float *)(PTR_DAT_00058da8 + (sVar1 + -1) * 4)) {
          for (sVar7 = 0; (int)sVar7 < sVar1 + -1; sVar7 = sVar7 + 1) {
            if ((*(float *)(PTR_DAT_00058da8 + sVar7 * 4) <= fVar9) &&
               (fVar9 < *(float *)(PTR_DAT_00058da8 + (sVar7 + 1) * 4))) {
              *PTR_Control_BaselineSourceFactorBin_00058da4 = (char)sVar7;
              break;
            }
          }
        }
        else {
          *PTR_Control_BaselineSourceFactorBin_00058da4 = (char)sVar1 + (char)DAT_00058d8c;
        }
      }
      else {
        *PTR_Control_BaselineSourceFactorBin_00058da4 = 0;
      }
      fVar9 = *(float *)(PTR_DAT_00058db4 + (uint)(byte)*puVar2 * 4);
      *(float *)PTR_Control_BaselineSourceSteppedFactor_00058db0 = fVar9;
      *(float *)PTR_Control_BaselineSourceTarget_00058dbc =
           (*(float *)puVar3 * fVar9) / DAT_00058db8;
      return &DAT_00058db8;
    }
  }
LAB_00058c0c:
  *(undefined4 *)PTR_Control_BaselineSourceTarget_00058c88 = 0;
  return puVar4;
}

