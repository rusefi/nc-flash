/* Ghidra analysis output; verify against original SH instructions. */

/* 8108 selectedbyabs72BC withstrict>50/>100/>200 thresholds:0/~.035/~.037/~.04.
   Independentof7242gate. */

undefined * Control_SelectSecondMagnitudeAmount(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined4 uVar3;
  float extraout_fr0;
  undefined4 uVar4;
  
  uVar4 = 0;
  uVar3 = (*(code *)PTR_FUN_00059698)(PTR_Control_SecondMagnitudeInput_000596d8);
  puVar1 = (undefined *)(*(code *)PTR_FUN_0005969c)(uVar3,uVar4);
  puVar2 = PTR_DAT_000596f0;
  if (extraout_fr0 <= *(float *)PTR_DAT_000596e0) {
    if (extraout_fr0 <= *(float *)PTR_DAT_000596e8) {
      if (extraout_fr0 <= *(float *)PTR_DAT_000596f0) {
        *(undefined4 *)PTR_Control_SecondMagnitudeAmount_000596dc = uVar4;
      }
      else {
        *(undefined4 *)PTR_Control_SecondMagnitudeAmount_000596dc = *(undefined4 *)PTR_DAT_000596f4;
      }
    }
    else {
      *(undefined4 *)PTR_Control_SecondMagnitudeAmount_000596dc = *(undefined4 *)PTR_DAT_000596ec;
      puVar2 = puVar1;
    }
  }
  else {
    *(undefined4 *)PTR_Control_SecondMagnitudeAmount_000596dc = *(undefined4 *)PTR_DAT_000596e4;
    puVar2 = puVar1;
  }
  return puVar2;
}

