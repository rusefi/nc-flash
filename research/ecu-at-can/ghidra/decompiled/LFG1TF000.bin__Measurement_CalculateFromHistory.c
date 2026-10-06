/* Ghidra analysis output; verify against original SH instructions. */

/* Both810C/9244 must be<18. Stale clears800C,resetsring,9238=7FFFFFFF,returns0. Healthy wrapped sum
   count=int16(param*24/360);period=sat32(sum*24)/count;result=clamp(153600000/period,0,32767).1536
   freshness/726 history cases; MACL preserved. See tcu-measurement.txt. */

int Measurement_CalculateFromHistory(short param_1)

{
  short sVar3;
  undefined4 uVar1;
  undefined4 uVar2;
  byte bVar4;
  int iVar5;
  int iVar6;
  int iVar7;
  
  uVar1 = DAT_000213d4;
  if (((byte)*PTR_Measurement_CurrentCaptureAge_000213d8 < (byte)*PTR_DAT_000213dc) &&
     (*(byte *)(int)DAT_000213ce < (byte)*PTR_DAT_000213dc)) {
    sVar3 = (*(code *)PTR_FixedPoint_DivideToSignedWord_000213e4)
                      ((int)(short)(ushort)(byte)*PTR_DAT_000213e0 * (int)param_1,(int)DAT_000213d0)
    ;
    iVar7 = 0;
    uVar1 = (*(code *)PTR_FUN_000213e8)();
    iVar6 = (int)sVar3;
    iVar5 = 0;
    bVar4 = Measurement_HistoryHead;
    if (0 < iVar6) {
      do {
        iVar7 = iVar7 + *(int *)(PTR_Measurement_CaptureHistory_000213ec + (uint)bVar4 * 4);
        if (bVar4 == 0) {
          bVar4 = *PTR_DAT_000213e0;
        }
        iVar5 = iVar5 + 1;
        bVar4 = bVar4 - 1;
      } while (iVar5 < iVar6);
    }
    (*(code *)PTR_FUN_000213f0)(uVar1);
    uVar1 = (*(code *)PTR_Arithmetic_SaturatingMultiplyShift_000213f4)(iVar7,*PTR_DAT_000213e0,0);
    uVar1 = (*(code *)PTR_Arithmetic_GuardedSignedDivision_000213f8)(uVar1,iVar6);
    iVar5 = (*(code *)PTR_Arithmetic_GuardedSignedDivision_000213f8)(DAT_000213fc,uVar1);
    if (DAT_000213d2 < iVar5) {
      iVar5 = (int)DAT_000213d2;
    }
    if (iVar5 < 0) {
      iVar5 = 0;
    }
  }
  else {
    sVar3 = (*(code *)PTR_FUN_00021404)();
    iVar5 = (int)sVar3;
    uVar2 = (*(code *)PTR_FUN_000213e8)();
    Measurement_CaptureCount = 0;
    (*(code *)PTR_FUN_000213f0)(uVar2);
    Measurement_ResetHistory();
  }
  *(undefined4 *)PTR_Measurement_NormalizedPeriod_00021408 = uVar1;
  return iVar5;
}

