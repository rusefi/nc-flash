/* Ghidra analysis output; verify against original SH instructions. */

/* Executed signedA552*6000/4100 clamp; unsigned scale1000; multiply91A2 then shift8/clampFFFF
   ->A5AC; A5B6=A5AC/100. Units unproven. */

void SpeedCandidate_CalculateForCAN216(void)

{
  ushort uVar1;
  undefined *puVar2;
  ushort uVar5;
  int iVar3;
  undefined4 uVar4;
  undefined2 uVar6;
  undefined4 in_r7;
  
  uVar1 = DAT_00052c02;
  if ((*PTR_DAT_00052c08 & 1) == 1) {
    uVar1 = *(ushort *)PTR_DAT_00052c0c;
  }
  uVar5 = (*(code *)PTR_FixedPoint_DivideToSignedWord_00052c18)
                    ((int)*(short *)PTR_SpeedCandidate_ScalingInput_00052c14 * (int)DAT_00052c04,
                     (int)*(short *)PTR_DAT_00052c10);
  iVar3 = (int)(short)uVar5;
  uVar4 = (*(code *)PTR_FUN_00052c1c)((uint)uVar5 * (uint)DAT_00052c02,(int)(short)uVar1);
  uVar6 = (*(code *)PTR_FUN_00052c24)
                    ((int)*(short *)PTR_Motion_PeriodDerivedValue_00052c20,uVar4,8,in_r7,iVar3);
  puVar2 = PTR_FUN_00052c2c;
  *(undefined2 *)PTR_CAN216_SpeedCandidate_00052c28 = uVar6;
  uVar6 = (*(code *)puVar2)();
  *(undefined2 *)PTR_DAT_00052c30 = uVar6;
  return;
}

