/* Ghidra analysis output; verify against original SH instructions. */

/* Ifabs7020>.9765625,80C0=max(813C,RTZ(RTZ(8098*6DB4)/7020));ordered15term
   sumthen81F8/8214subtractions,floor0to80BC. Elseholdboth.162cases andretainedpairedpipeline. */

uint Control_UpdateBaselineInput(void)

{
  undefined *puVar1;
  uint uVar2;
  float fVar3;
  undefined4 uVar4;
  undefined4 extraout_fr0;
  undefined4 uVar5;
  float fVar6;
  
  uVar5 = 0;
  fVar6 = *(float *)PTR_DAT_00058fd4;
  uVar2 = (*(code *)PTR_FUN_00058fdc)(fVar6,0,DAT_00058fd8);
  puVar1 = PTR_FUN_00058fe0;
  if ((uVar2 & 0xff) != 0) {
    fVar3 = (float)(*(code *)PTR_FUN_00058fe0)(PTR_DAT_00058fe4);
    uVar4 = (*(code *)PTR_FUN_00058ff0)
                      (*(undefined4 *)PTR_DAT_00058fec,
                       (*(float *)PTR_Control_ScaledRetainedBaselineSource_00058fe8 * fVar3) / fVar6
                      );
    *(undefined4 *)PTR_Control_BaselineScaledComponent_00058ff4 = uVar4;
    fVar3 = *(float *)PTR_Control_MappedBaselineContribution_00058ffc +
            *(float *)PTR_Control_LatchGatedBaselineContribution_00058ff8 +
            *(float *)PTR_Control_MagnitudeBaselineContribution_00059000 +
            *(float *)PTR_Control_NormalizedContribution_00059004 + *(float *)PTR_DAT_00059008 +
            *(float *)PTR_Control_BaselineScaledComponent_00058ff4 + *(float *)PTR_DAT_0005900c +
            *(float *)PTR_DAT_00059010;
    fVar6 = (float)(*(code *)puVar1)(PTR_DAT_00059014);
    fVar3 = fVar3 + fVar6;
    fVar6 = (float)(*(code *)puVar1)(PTR_DAT_00059018);
    fVar3 = fVar3 + fVar6 + *(float *)PTR_DAT_0005901c;
    fVar6 = (float)(*(code *)puVar1)(PTR_DAT_00059020);
    uVar2 = (*(code *)PTR_FUN_00058ff0)
                      (((fVar3 + fVar6 + *(float *)PTR_DAT_00059024 + *(float *)PTR_DAT_00059028 +
                        *(float *)PTR_DAT_0005902c) - *(float *)PTR_DAT_00059030) -
                       *(float *)PTR_DAT_00059034,uVar5);
    *(undefined4 *)PTR_Control_BaselineInput_00059038 = extraout_fr0;
  }
  return uVar2;
}

