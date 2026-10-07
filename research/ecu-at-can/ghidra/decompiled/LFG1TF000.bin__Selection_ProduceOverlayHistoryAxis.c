/* Ghidra analysis output; verify against original SH instructions. */

/* WARNING: Removing unreachable block (ram,0x00045c0a) */
/* Five-word9BE0 history shift/filter via10FAC; nonnegative lag difference saturated32767 into9B66.
   Reset history/current unless92C5bit2 andfilter>=signed80EA.1125direct+4endpoints+11retained;
   tcu-overlay-lifecycle.txt. */

void Selection_ProduceOverlayHistoryAxis(void)

{
  undefined *puVar1;
  int iVar2;
  short sVar3;
  short sVar4;
  short *psVar5;
  int iVar6;
  short *psVar7;
  undefined4 *puVar8;
  undefined4 local_28;
  undefined4 local_24;
  undefined4 local_20;
  undefined4 local_1c;
  short *local_18;
  
  sVar4 = DAT_ffff80ea;
  iVar2 = (int)DAT_ffff80ea;
  psVar7 = (short *)(int)DAT_00045cb4;
  local_18 = psVar7 + 4;
  *local_18 = psVar7[3];
  psVar5 = psVar7 + 1;
  psVar7[3] = psVar7[2];
  psVar7[2] = *psVar5;
  puVar1 = PTR_DAT_00045cb8;
  *psVar5 = *psVar7;
  sVar3 = (*(code *)PTR_Filter_UpdateSignedWordTowardInput_00045cbc)
                    ((int)*psVar5,iVar2,(uint)(byte)*puVar1 << 7);
  *psVar7 = sVar3;
  iVar2 = 1;
  iVar6 = (int)*local_18 - (int)*psVar7;
  local_1c = 0;
  local_20 = DAT_00045cc0;
  puVar8 = &local_20;
  sVar3 = (*(code *)PTR_FUN_00045cc8)();
  if (iVar6 < sVar3) {
    if (iVar2 == 0) {
      local_28 = DAT_00045cc4;
    }
    else {
      local_28 = DAT_00045cc0;
    }
    local_24 = 0;
    puVar8 = &local_28;
    sVar3 = (*(code *)PTR_FUN_00045cc8)();
    iVar6 = (int)sVar3;
  }
  if (((*PTR_DAT_00045ccc & 4) == 0) || (*(short *)(int)DAT_00045cb4 < sVar4)) {
    *psVar7 = sVar4;
    psVar7[1] = sVar4;
    psVar7[2] = sVar4;
    psVar7[3] = sVar4;
    psVar7[4] = sVar4;
    if (iVar2 == 0) {
      *(undefined4 *)((int)puVar8 + -4) = 0;
      *(undefined4 *)((int)puVar8 + -8) = DAT_00045cc4;
    }
    else {
      *(undefined4 *)((int)puVar8 + -4) = 0;
      *(undefined4 *)((int)puVar8 + -8) = DAT_00045cc0;
    }
    sVar4 = (*(code *)PTR_FUN_00045cc8)();
    iVar6 = (int)sVar4;
  }
  if (iVar6 < 0) {
    sVar4 = (*(code *)PTR_FUN_00045cd4)(iVar6,DAT_00045cd0);
    sVar3 = (short)DAT_00045cd0;
  }
  else {
    sVar4 = (*(code *)PTR_FUN_00045cd8)(iVar6,DAT_00045cd0);
    sVar3 = (short)DAT_00045cdc;
  }
  *(short *)PTR_Selection_OverlayHistoryAxis_00045ce0 = sVar3 + sVar4;
  return;
}

