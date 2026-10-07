/* Ghidra analysis output; verify against original SH instructions. */

/* Recognized4055=1/4/8 writesF858=18/1B/2Bhex; statusF859 low-nibble|20 afterclearbit20. OriginalSR
   helpers execute; no conversion/timing model. */

uint Acquisition_ConfigureBank2(void)

{
  undefined *puVar1;
  uint uVar2;
  int iVar3;
  undefined1 *puVar4;
  byte *pbVar5;
  undefined4 uStack_24;
  undefined4 uStack_20;
  undefined4 auStack_1c [2];
  
  puVar1 = PTR_FUN_000053a8;
  iVar3 = (int)DAT_00005398;
  puVar4 = (undefined1 *)(int)sRam0000539a;
  uVar2 = (uint)*(byte *)(iRam000053b0 + 2);
  pbVar5 = puVar4 + 1;
  if (uVar2 == 8) {
    (*(code *)PTR_FUN_000053ac)(auStack_1c,iVar3);
    *pbVar5 = *pbVar5 & 0xdf;
    *puVar4 = 0x2b;
    *pbVar5 = *pbVar5 & 0x2f | 0x20;
    uStack_24 = auStack_1c[0];
  }
  else if (uVar2 == 4) {
    (*(code *)PTR_FUN_000053ac)(&uStack_20,iVar3);
    *pbVar5 = *pbVar5 & 0xdf;
    *puVar4 = 0x1b;
    *pbVar5 = *pbVar5 & 0x2f | 0x20;
    uStack_24 = uStack_20;
  }
  else {
    if (uVar2 != 1) {
      return uVar2;
    }
    (*(code *)PTR_FUN_000053ac)(&uStack_24,iVar3);
    *pbVar5 = *pbVar5 & 0xdf;
    *puVar4 = 0x18;
    *pbVar5 = *pbVar5 & 0x2f | 0x20;
  }
  uVar2 = (*(code *)puVar1)(uStack_24);
  return uVar2;
}

