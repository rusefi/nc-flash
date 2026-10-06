/* Ghidra analysis output; verify against original SH instructions. */

/* 7012exact1 updates8090=A35D4(6DB4),807C=max(8090,8078);otherwise807C0and8090held. */

uint Control_SelectInputHistoryLimit(void)

{
  uint uVar1;
  undefined4 uVar2;
  undefined4 extraout_fr0;
  
  uVar1 = (*(code *)PTR_FUN_00058914)(PTR_DAT_0005893c);
  uVar1 = uVar1 & 0xff;
  if (uVar1 == 1) {
    uVar2 = (*(code *)PTR_FUN_00058930)(PTR_DAT_0005892c);
    uVar2 = (*(code *)PTR_Lookup_FloatCurve_00058938)(uVar2,DAT_00058940);
    *(undefined4 *)PTR_Control_InputLimitMapOutput_00058944 = uVar2;
    uVar1 = (*(code *)PTR_FUN_00058920)
                      (uVar2,*(undefined4 *)PTR_Control_RetainedInputLimit_00058908);
    *(undefined4 *)PTR_Control_ActiveInputLimit_00058948 = extraout_fr0;
  }
  else {
    *(undefined4 *)PTR_Control_ActiveInputLimit_00058948 = 0;
  }
  return uVar1;
}

