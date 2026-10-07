/* Ghidra analysis output; verify against original SH instructions. */

/* Recognized404F1/4/8/12 writesF818=10/13/23/33hex; F819 clearbit20 thenlow-nibble|20.
   Original22E4/22F4 execute; explicit control latches, no conversion model. */

uint Acquisition_ConfigureBank0(void)

{
  code *pcVar1;
  uint uVar2;
  int iVar3;
  undefined1 *puVar4;
  byte *pbVar5;
  undefined4 uStack_28;
  undefined4 uStack_24;
  undefined4 uStack_20;
  undefined4 auStack_1c [2];
  
  pcVar1 = pcRam00005130;
  iVar3 = (int)sRam00005128;
  puVar4 = (undefined1 *)(int)sRam0000512a;
  uVar2 = (uint)*(byte *)(iRam00005138 + 2);
  pbVar5 = puVar4 + 1;
  if (uVar2 == 0xc) {
    (*pcRam00005134)(auStack_1c,iVar3);
    *pbVar5 = *pbVar5 & 0xdf;
    *puVar4 = 0x33;
    *pbVar5 = *pbVar5 & 0x2f | 0x20;
    uStack_28 = auStack_1c[0];
  }
  else if (uVar2 == 8) {
    (*pcRam00005134)(&uStack_20,iVar3);
    *pbVar5 = *pbVar5 & 0xdf;
    *puVar4 = 0x23;
    *pbVar5 = *pbVar5 & 0x2f | 0x20;
    uStack_28 = uStack_20;
  }
  else if (uVar2 == 4) {
    (*pcRam00005134)(&uStack_24,iVar3);
    *pbVar5 = *pbVar5 & 0xdf;
    *puVar4 = 0x13;
    *pbVar5 = *pbVar5 & 0x2f | 0x20;
    uStack_28 = uStack_24;
  }
  else {
    if (uVar2 != 1) {
      return uVar2;
    }
    (*pcRam00005134)(&uStack_28,iVar3);
    *pbVar5 = *pbVar5 & 0xdf;
    *puVar4 = 0x10;
    *pbVar5 = *pbVar5 & 0x2f | 0x20;
  }
  uVar2 = (*pcVar1)(uStack_28);
  return uVar2;
}

