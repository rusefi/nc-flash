/* Ghidra analysis output; verify against original SH instructions. */

/* Any nonzero protected7002 clears6808; else ordered RTZ sum6818+6820+6824 clamped0..680C.
   Cancellation and raw flags tested. */

uint Control_SumBoundedInputTerms(void)

{
  uint uVar1;
  float fVar2;
  undefined4 extraout_fr0;
  undefined4 uVar3;
  
  uVar3 = 0;
  uVar1 = (*(code *)PTR_FUN_0003148c)(PTR_DAT_00031488);
  uVar1 = uVar1 & 0xff;
  if (uVar1 == 0) {
    fVar2 = (float)(*(code *)PTR_FUN_00031494)(PTR_Control_ScaledErrorTerm_00031490);
    uVar1 = (*(code *)PTR_FUN_00031478)
                      (fVar2 + *(float *)PTR_Control_AccumulatedErrorTerm_00031498 +
                       *(float *)PTR_Control_ScaledDifferenceTerm_0003149c,uVar3,
                       *(undefined4 *)PTR_Control_InputTermSumLimit_000314a0);
    *(undefined4 *)PTR_Control_BoundedInputTermSum_000314a4 = extraout_fr0;
  }
  else {
    *(undefined4 *)PTR_Control_BoundedInputTermSum_000314a4 = uVar3;
  }
  return uVar1;
}

