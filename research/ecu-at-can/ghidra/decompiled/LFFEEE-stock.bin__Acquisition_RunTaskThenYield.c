/* Ghidra analysis output; verify against original SH instructions. */

/* Executed20 explicit task7/priority3 queuedcycles after38C4
   initialization:391A->3B8A/3D10/RTE->E26C->3CB8 consumption->3D0C idle.4CE2->6718
   and215B4/17D88->1DF32 execute. ADC1 copies/scales atcycle1;ADC28 copiesat16 butfull3976C
   decoderabsent. Low-level requests, notphysical cadence/produceradmission. Earlierdirectcall
   failures retained; control-task-dispatch.txt. */

undefined4 Acquisition_RunTaskThenYield(void)

{
  ushort *puVar1;
  code *pcVar2;
  code *pcVar3;
  undefined *puVar4;
  undefined4 uVar5;
  int iVar6;
  ushort *puVar7;
  undefined4 uStack_14;
  undefined4 uStack_10;
  undefined4 uStack_c;
  ushort *puStack_8;
  
  (*(code *)PTR_LAB_0000e340)();
  (*(code *)PTR_Acquisition_CopyAndScheduleBanks_0000e344)();
  (*pcRam0000e348)();
  (*pcRam0000e34c)();
  (*pcRam0000e350)();
  (*(code *)PTR_LAB_0000e354)();
  (*(code *)PTR_LAB_0000e358)();
  (*(code *)PTR_SCI1_ServiceTimeoutAndMonitor_0000e35c)();
  (*(code *)PTR_LAB_0000e360)();
  (*(code *)PTR_LAB_0000e364)();
  pcVar2 = pcRam0000e36c;
  puVar1 = puRam0000e368;
  iVar6 = (int)sRam0000e2f8;
  *puRam0000e368 = *puRam0000e368 + 1;
  (*pcVar2)(&uStack_c,iVar6);
  pcVar3 = pcRam0000e370;
  iVar6 = (int)sRam0000e2fa;
  if (*puVar1 < puVar1[1]) {
    if (puVar1[3] <= *puVar1) {
      (*pcRam0000e370)(iVar6,0x10,0);
    }
  }
  else {
    *puVar1 = 0;
    puVar1[3] = puVar1[4];
    puVar1[1] = puVar1[2];
    if ((*(char *)(puVar1 + 5) == '\0') && (puVar1[3] != 0)) {
      (*pcVar3)(iVar6,0x10,1);
    }
  }
  puVar4 = PTR_FUN_0000e4ac;
  (*(code *)PTR_FUN_0000e4ac)(uStack_c);
  iVar6 = (int)sRam0000e4a6;
  puStack_8 = puVar1 + 0xc;
  *puStack_8 = *puStack_8 + 1;
  (*pcVar2)(&uStack_10,iVar6);
  iVar6 = (int)sRam0000e4a8;
  if (*puStack_8 < puStack_8[1]) {
    if (puVar1[0xf] <= puVar1[0xc]) {
      (*pcVar3)(iVar6,0x20,0);
    }
  }
  else {
    puVar1[0xc] = 0;
    puVar1[0xf] = puVar1[0x10];
    puVar1[0xd] = puVar1[0xe];
    if ((*(char *)(puVar1 + 0x11) == '\0') && (puVar1[0xf] != 0)) {
      (*pcVar3)(iVar6,0x20,1);
    }
  }
  (*(code *)puVar4)(uStack_10);
  iVar6 = (int)sRam0000e4a6;
  puVar7 = puVar1 + 6;
  *puVar7 = *puVar7 + 1;
  (*pcVar2)(&uStack_14,iVar6);
  iVar6 = (int)sRam0000e4aa;
  if (*puVar7 < puVar1[7]) {
    if (puVar1[9] <= puVar1[6]) {
      (*pcVar3)(iVar6,0x10,0);
    }
  }
  else {
    puVar1[6] = 0;
    puVar1[9] = puVar1[10];
    puVar1[7] = puVar1[8];
    if ((*(char *)(puVar1 + 0xb) == '\0') && (puVar1[9] != 0)) {
      (*pcVar3)(iVar6,0x10,1);
    }
  }
  (*(code *)puVar4)(uStack_14);
  uVar5 = (*(code *)PTR_LAB_0000e4b0)();
  return uVar5;
}

