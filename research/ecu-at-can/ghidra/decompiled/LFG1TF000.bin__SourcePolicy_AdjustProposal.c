/* Ghidra analysis output; verify against original SH instructions. */

/* 9316bit0 admission through498D2; writes9B40=17 if previous6 else10, executes496F0 proposal
   policy, publishes9C91/94/96 and9AEA flags. Blocked path preserves incoming pair/source.1152
   direct cases and640 observed full-caller updates; tcu-source-selection.txt. */

void SourcePolicy_AdjustProposal(undefined1 *param_1,undefined1 *param_2)

{
  bool bVar1;
  bool bVar2;
  undefined *puVar3;
  byte bVar4;
  char cVar7;
  int iVar5;
  ushort uVar6;
  undefined1 uVar8;
  byte bVar9;
  undefined1 local_30 [4];
  undefined1 auStack_2c [4];
  undefined1 *puStack_28;
  undefined1 *puStack_24;
  ushort uStack_20;
  
  bVar1 = false;
  bVar2 = false;
  local_30[0] = *param_2;
  uVar8 = *param_1;
  auStack_2c[0] = 0;
  bVar9 = *PTR_Selector_ApplicationFlags16_000496dc;
  *(short *)(int)DAT_000496d0 = DAT_ffff809c << 1;
  uStack_20 = DAT_ffff80ea;
  puStack_28 = param_1;
  puStack_24 = param_2;
  cVar7 = SourcePolicy_CheckAdmission(bVar9 & 1);
  if (cVar7 == '\x01') {
    uVar8 = 10;
    bVar1 = *PTR_Selection_SourceCode_000496e0 == '\x06';
    if (bVar1) {
      uVar8 = 0x11;
    }
    *PTR_Selection_SourceCode_000496e0 = uVar8;
    bVar4 = Selection_ApplicationIndex;
    iVar5 = (int)(char)Selection_ApplicationIndex;
    local_30[0] = *PTR_DAT_000496e4;
    bVar2 = true;
    if (*(char *)(int)DAT_000496ce == '\0') {
      *(undefined1 *)(int)DAT_000496ca = 0;
      *(undefined1 *)(int)DAT_000496cc = 0;
      if (((bVar4 != 0) &&
          (uVar6 = SourcePolicy_LookupDecrementThreshold(iVar5),
          *(ushort *)(int)DAT_000496d0 <
          *(ushort *)(PTR_SourcePolicy_EntryAxisBounds_000496e8 + (bVar4 - 1) * 2))) &&
         (uStack_20 < uVar6)) {
        iVar5 = iVar5 + -1;
        auStack_2c[0] = 1;
        local_30[0] = 10;
      }
    }
    uVar8 = SourcePolicy_ApplyThresholdRules(iVar5,auStack_2c,local_30);
  }
  puVar3 = PTR_DAT_000496ec;
  *(byte *)(int)DAT_000496ce = bVar9 & 1;
  *puStack_24 = local_30[0];
  *puStack_28 = uVar8;
  *PTR_SourcePolicy_AdjustmentState_000496d8 = auStack_2c[0];
  if (bVar2) {
    *puVar3 = *puVar3 | 2;
  }
  else {
    *puVar3 = *puVar3 & 0xfd;
  }
  if (bVar1) {
    bVar9 = *puVar3 | 8;
  }
  else {
    bVar9 = *puVar3 & 0xf7;
  }
  *puVar3 = bVar9;
  return;
}

