/* Ghidra analysis output; verify against original SH instructions. */

/* 718E clears if old714C>65535; sets if718C==1 and7190/7191==1; otherwise holds.64 cases verified.
    */

undefined4 * CAN211_UpdateRecoveryLatch(void)

{
  undefined4 *puVar1;
  uint uVar2;
  float fVar3;
  
  fVar3 = (float)(*(code *)PTR_FUN_0003fe84)(PTR_CAN211_NumericBound_0003fe80);
  puVar1 = &DAT_0003fe88;
  if (fVar3 <= DAT_0003fe88) {
    uVar2 = (*(code *)PTR_FUN_0003fe48)(PTR_DAT_0003fe90);
    puVar1 = (undefined4 *)(uVar2 & 0xff);
    if ((puVar1 == (undefined4 *)0x1) &&
       ((puVar1 = (undefined4 *)0x1, *PTR_DAT_0003fe94 == '\x01' ||
        (puVar1 = (undefined4 *)(uint)(byte)*PTR_DAT_0003fe7c, puVar1 == (undefined4 *)0x1)))) {
      *PTR_DAT_0003fe8c = 1;
    }
  }
  else {
    *PTR_DAT_0003fe8c = 0;
  }
  return puVar1;
}

