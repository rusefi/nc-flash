/* Ghidra analysis output; verify against original SH instructions. */

/* Likebank0 atF838/F839 using4052; addsconfigbit40 exactlywhen4049==1. Allcountbytes
   andflag0/1/2/255 tested. No hardwarecompletion or sensoridentity claim. */

uint Acquisition_ConfigureBank1(void)

{
  code *pcVar1;
  uint uVar2;
  int iVar3;
  undefined1 *puVar4;
  byte *pbVar5;
  undefined4 uStack_38;
  undefined4 uStack_34;
  undefined4 uStack_30;
  undefined4 uStack_2c;
  undefined4 uStack_28;
  undefined4 uStack_24;
  undefined4 uStack_20;
  undefined4 auStack_1c [2];
  
  pcVar1 = pcRam00005130;
  iVar3 = (int)sRam00005128;
  puVar4 = (undefined1 *)(int)sRam0000512c;
  pbVar5 = puVar4 + 1;
  if (*pcRam00005140 == '\x01') {
    uVar2 = (uint)*(byte *)(iRam0000513c + 2);
    if (uVar2 == 0xc) {
      (*pcRam00005134)(auStack_1c,iVar3);
      *pbVar5 = *pbVar5 & 0xdf;
      *puVar4 = 0x73;
      *pbVar5 = *pbVar5 & 0x2f | 0x20;
      uStack_28 = auStack_1c[0];
    }
    else if (uVar2 == 8) {
      (*pcRam00005134)(&uStack_20,iVar3);
      *pbVar5 = *pbVar5 & 0xdf;
      *puVar4 = 99;
      *pbVar5 = *pbVar5 & 0x2f | 0x20;
      uStack_28 = uStack_20;
    }
    else if (uVar2 == 4) {
      (*pcRam00005134)(&uStack_24,iVar3);
      *pbVar5 = *pbVar5 & 0xdf;
      *puVar4 = 0x53;
      *pbVar5 = *pbVar5 & 0x2f | 0x20;
      uStack_28 = uStack_24;
    }
    else {
      if (uVar2 != 1) {
        return uVar2;
      }
      (*pcRam00005134)(&uStack_28,iVar3);
      *pbVar5 = *pbVar5 & 0xdf;
      *puVar4 = 0x50;
      *pbVar5 = *pbVar5 & 0x2f | 0x20;
    }
    uVar2 = (*pcVar1)(uStack_28);
  }
  else {
    uVar2 = (uint)*(byte *)(iRam0000513c + 2);
    if (uVar2 == 0xc) {
      (*pcRam00005134)(&uStack_2c,iVar3);
      *pbVar5 = *pbVar5 & 0xdf;
      *puVar4 = 0x33;
      *pbVar5 = *pbVar5 & 0x2f | 0x20;
      uStack_38 = uStack_2c;
    }
    else if (uVar2 == 8) {
      (*pcRam00005134)(&uStack_30,iVar3);
      *pbVar5 = *pbVar5 & 0xdf;
      *puVar4 = 0x23;
      *pbVar5 = *pbVar5 & 0x2f | 0x20;
      uStack_38 = uStack_30;
    }
    else if (uVar2 == 4) {
      (*pcRam00005134)(&uStack_34,iVar3);
      *pbVar5 = *pbVar5 & 0xdf;
      *puVar4 = 0x13;
      *pbVar5 = *pbVar5 & 0x2f | 0x20;
      uStack_38 = uStack_34;
    }
    else {
      if (uVar2 != 1) {
        return uVar2;
      }
      (*pcRam00005134)(&uStack_38,iVar3);
      *pbVar5 = *pbVar5 & 0xdf;
      *puVar4 = 0x10;
      *pbVar5 = *pbVar5 & 0x2f | 0x20;
    }
    uVar2 = (*pcVar1)(uStack_38);
  }
  return uVar2;
}

