/* Ghidra analysis output; verify against original SH instructions. */

/* 680C priority: zero if693Dzero and6910positive; elsemode7016zero/timerpositive curve; else scaled
   target, .08 rising slew for modezero,7010exact1 override for nonzero
   mode.2022cases/24callersegments/320cycles. */

uint Control_ProduceInputTermSumLimit(void)

{
  ushort uVar1;
  undefined *puVar2;
  undefined *puVar3;
  char cVar5;
  uint uVar4;
  char cVar6;
  float extraout_fr0;
  float fVar7;
  float fVar8;
  float extraout_fr0_00;
  float fVar9;
  float fVar10;
  float fVar11;
  
  puVar2 = PTR_Control_InputTermSumLimit_000314a0;
  fVar10 = *(float *)PTR_Control_AccumulatedErrorLimit_000314a8;
  fVar11 = *(float *)PTR_Control_InputTermSumLimit_000314a0;
  fVar9 = *(float *)PTR_Control_InputLimitFactor_000314ac;
  uVar1 = *(ushort *)PTR_ControlInput_LimitCountdown_000314b0;
  cVar5 = (*(code *)PTR_FUN_0003148c)(PTR_DAT_000314b4);
  puVar3 = PTR_DAT_000314c8;
  if ((*PTR_ControlInput_MappedHysteresisGate_000314b8 == '\0') && (uVar4 = (uint)uVar1, uVar4 != 0)
     ) {
    *(undefined4 *)puVar2 = 0;
  }
  else if ((cVar5 == '\0') && (uVar1 != 0)) {
    uVar4 = (*(code *)PTR_Lookup_FloatCurve_000314c4)
                      (*(undefined4 *)PTR_ControlInput_NormalizedLimitRatio_000314bc,
                       PTR_PTR_000314c0);
    *(float *)puVar2 = fVar10 * extraout_fr0;
  }
  else {
    cVar6 = (*(code *)PTR_FUN_000314d4)
                      (*(undefined4 *)PTR_DAT_000314d0,*(undefined4 *)PTR_DAT_000314c8,DAT_000314cc)
    ;
    fVar8 = fVar11;
    if (cVar6 != '\0') {
      fVar7 = (float)(*(code *)PTR_FUN_00031494)(PTR_DAT_000314d8);
      fVar8 = fVar9;
      if (cVar5 == '\0') {
        fVar8 = 1.0;
      }
      fVar8 = (float)(*(code *)PTR_FUN_00031478)
                               ((fVar7 - *(float *)puVar3) /
                                (*(float *)PTR_DAT_000314d0 - *(float *)puVar3),
                                *(undefined4 *)PTR_DAT_000314dc,fVar8);
      fVar8 = fVar8 * fVar10;
    }
    if (cVar5 == '\0') {
      uVar4 = (*(code *)PTR_FUN_000314e4)(*(float *)PTR_DAT_000314e0 + fVar11,fVar8);
      fVar8 = extraout_fr0_00;
    }
    else {
      uVar4 = (*(code *)PTR_FUN_0003148c)(PTR_DAT_000314e8);
      uVar4 = uVar4 & 0xff;
      if (uVar4 == 1) {
        fVar8 = fVar10 * fVar9;
      }
    }
    *(float *)puVar2 = fVar8;
  }
  return uVar4;
}

