/* Ghidra analysis output; verify against original SH instructions. */

/* 9315 low2bits reset progress/rates;otherwise70B39(9334)>>8 ->9718,328FC
   updatesselectedrates,32C2C integrates signedoldwords.971Abit0 cleared then conditionallyset;
   otherbits preserved.832 complete-body cases; tcu-transition-progress.txt. */

void TransitionProgress_Update(void)

{
  short sVar1;
  short sVar2;
  short sVar3;
  undefined *puVar4;
  ushort extraout_var;
  undefined2 uVar5;
  undefined2 uVar6;
  undefined2 uVar7;
  undefined4 *puVar8;
  undefined4 *puVar9;
  byte *pbVar10;
  
  sVar1 = *(short *)PTR_TransitionProgress_AccumulatorA_00032400;
  sVar2 = *(short *)PTR_TransitionProgress_AccumulatorB_00032404;
  sVar3 = *(short *)PTR_TransitionProgress_AccumulatorC_00032408;
  pbVar10 = (byte *)(int)DAT_000323f6;
  if (((PTR_DAT_0003240c[1] & 1) == 0) && ((PTR_DAT_0003240c[1] & 2) == 0)) {
    *pbVar10 = *pbVar10 & 0xfe;
    (*(code *)PTR_Lookup_ByteCurveToFixedPoint_00032418)
              ((int)*(short *)PTR_CutLookup_Axis_00032414,
               PTR_TransitionProgress_RateScaleCurve_00032410);
    *(ushort *)(int)DAT_000323f8 = extraout_var & 0xff;
    TransitionProgress_SelectRates();
    uVar5 = TransitionProgress_AccumulateAndClamp(0,(int)sVar1,*(undefined4 *)(int)DAT_000323fa);
    uVar6 = TransitionProgress_AccumulateAndClamp(0,(int)sVar2,*(undefined4 *)(int)DAT_000323fc);
    uVar7 = TransitionProgress_AccumulateAndClamp
                      (*pbVar10 & 1,(int)sVar3,*(undefined4 *)(int)DAT_000323fe);
  }
  else {
    uVar7 = 0;
    uVar5 = 0;
    puVar9 = (undefined4 *)(int)DAT_000323fc;
    uVar6 = 0;
    puVar8 = (undefined4 *)(int)DAT_000323fe;
    *(undefined4 *)(int)DAT_000323fa = 0;
    *puVar9 = 0;
    *puVar8 = 0;
    *pbVar10 = *pbVar10 & 0xfe;
  }
  puVar4 = PTR_TransitionProgress_AccumulatorB_00032404;
  *(undefined2 *)PTR_TransitionProgress_AccumulatorA_00032400 = uVar5;
  *(undefined2 *)puVar4 = uVar6;
  *(undefined2 *)PTR_TransitionProgress_AccumulatorC_00032408 = uVar7;
  return;
}

