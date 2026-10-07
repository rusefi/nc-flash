/* Ghidra analysis output; verify against original SH instructions. */

/* 6814 map A38DC(67DC) if6938exact1, elsezero; any67C4 caps65.540cases. control-input-limits.txt.
    */

uint Control_ProduceAccumulatedErrorLimit(void)

{
  undefined *puVar1;
  uint uVar2;
  undefined4 extraout_fr0;
  undefined4 extraout_fr0_00;
  
  puVar1 = PTR_Control_AccumulatedErrorLimit_000316a8;
  uVar2 = (uint)(byte)*PTR_ControlInput_ScaleHysteresisGate_000316ac;
  if (uVar2 == 1) {
    uVar2 = (*(code *)PTR_Lookup_FloatCurve_000316b8)
                      (*(undefined4 *)PTR_ControlInput_ScaledLimitAxis_000316b0,PTR_LAB_000316b4);
    if (*PTR_DAT_000316bc == '\0') {
      *(undefined4 *)puVar1 = extraout_fr0;
    }
    else {
      uVar2 = (*(code *)PTR_FUN_000316c4)(extraout_fr0,*(undefined4 *)PTR_DAT_000316c0);
      *(undefined4 *)puVar1 = extraout_fr0_00;
    }
  }
  else {
    *(undefined4 *)PTR_Control_AccumulatedErrorLimit_000316a8 = 0;
  }
  return uVar2;
}

