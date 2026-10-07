/* Ghidra analysis output; verify against original SH instructions. */

/* 692B reload100on695Bbit4 elsedecrement.693F clearsat6828>=.9*6814 ANDtimer0;setsat6828<=upper-5
   ANDprotected2160>=93;elseholds. Inclusivebounds andexpiredholdverified. */

undefined4 TargetFollow_UpdateSecondLatch(void)

{
  undefined4 uVar1;
  float extraout_fr0;
  float fVar2;
  float fVar3;
  float fVar4;
  float fVar5;
  
  fVar5 = *(float *)PTR_TargetFollow_FilteredContribution_00031dec;
  fVar2 = *(float *)PTR_DAT_00031df0;
  fVar3 = *(float *)PTR_Control_AccumulatedErrorLimit_00031df4;
  fVar4 = fVar3 * fVar2 - *(float *)PTR_DAT_00031df8;
  if ((*PTR_ControlMode_SelectedBit_00031ddc & 0x10) == 0) {
    if (*PTR_TargetFollow_SecondCountdown_00031dfc != '\0') {
      *PTR_TargetFollow_SecondCountdown_00031dfc =
           *PTR_TargetFollow_SecondCountdown_00031dfc + (char)DAT_00031eb2;
    }
  }
  else {
    *PTR_TargetFollow_SecondCountdown_00031dfc = *PTR_DAT_00031e00;
  }
  if ((fVar5 < fVar3 * fVar2) || (*PTR_TargetFollow_SecondCountdown_00031eb4 != '\0')) {
    uVar1 = (*(code *)PTR_FUN_00031ec4)(*(undefined4 *)PTR_DAT_00031ebc,PTR_DAT_00031ec0);
    if ((*(float *)PTR_DAT_00031ec8 <= extraout_fr0) && (fVar5 <= fVar4)) {
      *PTR_TargetFollow_SecondRetainedFlag_00031eb8 = 1;
    }
  }
  else {
    uVar1 = 0;
    *PTR_TargetFollow_SecondRetainedFlag_00031eb8 = 0;
  }
  return uVar1;
}

