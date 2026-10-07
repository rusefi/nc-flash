/* Ghidra analysis output; verify against original SH instructions. */

/* Copies ten48-byte curves from7422C into9CA8. For i<5 with9F29bit1 and8081=i, replaces rowi with
   rowi+5. Copy executes before higher-priority bank overrides;891 full-copy checks in
   tcu-curve-sources.txt. */

undefined4 Selection_CopyDynamicCurves(void)

{
  undefined *puVar1;
  undefined4 uVar2;
  int iVar3;
  int iVar4;
  uint uVar5;
  
  puVar1 = PTR_FUN_0004a718;
  uVar5 = 0;
  do {
    iVar4 = uVar5 * 0x30;
    if ((int)uVar5 < 5) {
      iVar3 = iVar4;
      if (((*(byte *)(int)DAT_0004a70e & 2) != 0) && (CAN231_SixStateSource == uVar5)) {
        iVar3 = (uVar5 + 5) * 0x30;
      }
      uVar2 = (*(code *)puVar1)(PTR_DAT_0004a720 + iVar4,
                                PTR_WORD_ARRAY_0007404c_240__0004a71c + iVar3,0x30);
    }
    else {
      uVar2 = (*(code *)puVar1)(PTR_DAT_0004a720 + iVar4,
                                PTR_WORD_ARRAY_0007404c_240__0004a71c + iVar4,0x30);
    }
    uVar5 = uVar5 + 1;
  } while ((int)uVar5 < 10);
  return uVar2;
}

