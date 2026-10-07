/* Ghidra analysis output; verify against original SH instructions. */

/* Group5D3BC ->record ackbytes0..9; requiredmetadata0 latches+14; exact1 latch plusallnonzero
   permitshead/thentail retirement with3callbacks. Prior4096bitmap/975statefulcases; new4132wholeRAM
   directcases and85 actualreturn wholeRAM checks in32+352 fulltasks. tcu-initialized-requests.txt.
   Native-startup320 periods add27 actualreturn wholeRAM checks; thirdphaseindex2/group6/code9
   remains at320. tcu-native-can-lifecycle.txt. */

undefined4 Phase_AcknowledgeAndRetire(byte param_1,short param_2)

{
  undefined1 uVar1;
  int iVar2;
  bool bVar3;
  undefined *puVar4;
  undefined *puVar5;
  ushort uVar7;
  undefined4 uVar6;
  code *pcVar8;
  short sVar9;
  undefined4 *puVar10;
  undefined4 *puVar11;
  
  puVar4 = PTR_Phase_RecordRing_00031cb4;
  sVar9 = 0;
  iVar2 = (uint)param_1 * 0xf;
  do {
    if (param_2 == *(short *)(PTR_Request_PeriodicGroupRecords_00031cb0 + sVar9 * 4)) {
      if (param_1 < 0x10) {
        PTR_Phase_RecordRing_00031cb4[sVar9 + iVar2] = 1;
      }
      break;
    }
    sVar9 = sVar9 + 1;
  } while (sVar9 < 10);
  if (puVar4[iVar2 + 0xe] == '\0') {
    bVar3 = true;
    sVar9 = 0;
    do {
      if ((puVar4[sVar9 + iVar2] == '\0') &&
         (PTR_Request_PeriodicGroupRecords_2__00031cb8[sVar9 * 4] == '\0')) {
        bVar3 = false;
        break;
      }
      sVar9 = sVar9 + 1;
    } while (sVar9 < 10);
    if (bVar3) {
      puVar4[iVar2 + 0xe] = 1;
    }
  }
  puVar5 = PTR_Phase_RetirementCallbacks_00031d90;
  puVar10 = (undefined4 *)(PTR_Phase_RetirementCallbacks_00031d90 + 0xc);
  while ((puVar4[DAT_00031d8c] != '\0' &&
         (puVar4[(uint)(byte)puVar4[DAT_00031d8a] * 0xf + 0xe] == '\x01'))) {
    bVar3 = true;
    sVar9 = 0;
    do {
      if (puVar4[(int)sVar9 + (uint)(byte)puVar4[DAT_00031d8a] * 0xf] == '\0') {
        bVar3 = false;
        break;
      }
      sVar9 = sVar9 + 1;
    } while (sVar9 < 10);
    if (!bVar3) break;
    uVar1 = puVar4[(uint)(byte)puVar4[DAT_00031d8a] * 0xf + 10];
    puVar11 = (undefined4 *)puVar5;
    do {
      pcVar8 = (code *)*puVar11;
      puVar11 = puVar11 + 1;
      (*pcVar8)(uVar1);
    } while (puVar11 < puVar10);
    puVar4[DAT_00031d8a] = puVar4[DAT_00031d8a] + 0x11 & 0xf;
    puVar4[DAT_00031d8c] = puVar4[DAT_00031d8c] + -1;
  }
  while ((puVar4[DAT_00031ea8] != 0 &&
         (uVar7 = (ushort)(byte)puVar4[DAT_00031eaa] + (ushort)(byte)puVar4[DAT_00031ea8] + 0xf &
                  0xf, puVar4[(short)uVar7 * 0xf + 0xe] == '\x01'))) {
    bVar3 = true;
    sVar9 = 0;
    do {
      if (puVar4[(int)sVar9 + (short)uVar7 * 0xf] == '\0') {
        bVar3 = false;
        break;
      }
      sVar9 = sVar9 + 1;
    } while (sVar9 < 10);
    if (!bVar3) break;
    uVar1 = puVar4[(short)uVar7 * 0xf + 10];
    puVar10 = (undefined4 *)puVar5;
    do {
      pcVar8 = (code *)*puVar10;
      puVar10 = puVar10 + 1;
      (*pcVar8)(uVar1);
    } while (puVar10 < puVar5 + 0xc);
    puVar4[DAT_00031ea8] = puVar4[DAT_00031ea8] + -1;
  }
  if (puVar4[DAT_00031ea8] == '\0') {
    *(undefined1 *)(int)DAT_00031eac = 0;
    uVar6 = 1;
  }
  else {
    uVar6 = 0xffffffff;
  }
  return uVar6;
}

