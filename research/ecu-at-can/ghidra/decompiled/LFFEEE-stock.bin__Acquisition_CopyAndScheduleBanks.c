/* Ghidra analysis output; verify against original SH instructions. */

/* Copies previous count selections, increments old-mode counters and byte phase; selects next12/8/0
   or every16th12/12/8. Everyfourth16th sets4049=1 withbytewrap. Executes nested SR/configuration
   helpers with explicit register latches, not conversion/timing. See
   control-acquisition-schedule.txt. */

uint Acquisition_CopyAndScheduleBanks(void)

{
  char cVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined4 uVar5;
  uint uVar6;
  int iVar7;
  undefined1 *puVar8;
  byte *pbVar9;
  undefined4 uStack_24;
  undefined4 uStack_20;
  undefined4 auStack_1c [2];
  
  Acquisition_CopyBank0();
  Acquisition_CopyBank1();
  Acquisition_CopyBank2();
  puVar3 = PTR_Acquisition_PreviousScanMode_00004d90;
  puVar2 = PTR_DAT_00004d8c;
  cVar1 = *PTR_Acquisition_PreviousScanMode_00004d90;
  if (cVar1 == '\x02') {
    PTR_DAT_00004d8c[2] = PTR_DAT_00004d8c[2] + '\x01';
code_r0x00004d1a:
    puVar2[1] = puVar2[1] + '\x01';
  }
  else {
    if (cVar1 == '\x01') goto code_r0x00004d1a;
    if (cVar1 != '\0') goto code_r0x00004d26;
  }
  *puVar2 = *puVar2 + '\x01';
code_r0x00004d26:
  puVar4 = PTR_Acquisition_ExtendedBankFlag_00004d98;
  puVar2 = PTR_Acquisition_ScanPhase_00004d94;
  iVar7 = DAT_00004d88;
  *PTR_Acquisition_ScanPhase_00004d94 = *PTR_Acquisition_ScanPhase_00004d94 + '\x01';
  *puVar4 = 0;
  if ((*puVar2 & 0xf) == 0) {
    *puVar3 = 2;
    puVar2 = PTR_Acquisition_SlowScanCounter_00004d9c;
    *(undefined1 *)(iVar7 + 2) = 0xc;
    *(undefined1 *)(iVar7 + 5) = 0xc;
    *(undefined1 *)(iVar7 + 8) = 8;
    *puVar2 = *puVar2 + '\x01';
    if (3 < (byte)*puVar2) {
      *PTR_Acquisition_ExtendedBankFlag_00004d98 = 1;
      *puVar2 = 0;
    }
  }
  else {
    if ((*puVar2 & 3) == 0) {
      *puVar3 = 1;
    }
    else {
      *puVar3 = 0;
    }
    *(undefined1 *)(iVar7 + 2) = 0xc;
    *(undefined1 *)(iVar7 + 5) = 8;
    *(undefined1 *)(iVar7 + 8) = 0;
  }
  if (*(char *)(iVar7 + 2) != '\0') {
    Acquisition_ConfigureBank0();
  }
  if (*(char *)(iVar7 + 5) != '\0') {
    uVar5 = (*pcRam00004ec8)((int)sRam00004eb2);
    *PTR_Acquisition_AlternateArmed_00004ecc = 0;
    Acquisition_ConfigureBank1();
    (*pcRam00004ed0)(uVar5);
  }
  puVar2 = PTR_FUN_000053a8;
  if (*(char *)(iVar7 + 8) != '\0') {
    iVar7 = (int)DAT_00005398;
    puVar8 = (undefined1 *)(int)sRam0000539a;
    uVar6 = (uint)*(byte *)(iRam000053b0 + 2);
    pbVar9 = puVar8 + 1;
    if (uVar6 == 8) {
      (*(code *)PTR_FUN_000053ac)(auStack_1c,iVar7);
      *pbVar9 = *pbVar9 & 0xdf;
      *puVar8 = 0x2b;
      *pbVar9 = *pbVar9 & 0x2f | 0x20;
      uStack_24 = auStack_1c[0];
    }
    else if (uVar6 == 4) {
      (*(code *)PTR_FUN_000053ac)(&uStack_20,iVar7);
      *pbVar9 = *pbVar9 & 0xdf;
      *puVar8 = 0x1b;
      *pbVar9 = *pbVar9 & 0x2f | 0x20;
      uStack_24 = uStack_20;
    }
    else {
      if (uVar6 != 1) {
        return uVar6;
      }
      (*(code *)PTR_FUN_000053ac)(&uStack_24,iVar7);
      *pbVar9 = *pbVar9 & 0xdf;
      *puVar8 = 0x18;
      *pbVar9 = *pbVar9 & 0x2f | 0x20;
    }
    uVar6 = (*(code *)puVar2)(uStack_24);
    return uVar6;
  }
  return 0;
}

