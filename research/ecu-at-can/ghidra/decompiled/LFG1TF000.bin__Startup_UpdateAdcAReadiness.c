/* Ghidra analysis output; verify against original SH instructions. */

/* 24960 independentwholeRAM/MMIO cases PASS:5C578/F810 count,16EFE->84A4/84A2. States1/2
   high>5525/>9000 qualify2/3;low<=3600 qualifies4. State3 low->4;state4
   high>5525->2;unsigned100000timestampcounts. Original12stepchain1/2/3/4/2/3 PASS. No
   physicalunits/caller/fullboot. tcu-readiness-a.txt. */

uint Startup_UpdateAdcAReadiness(void)

{
  undefined *puVar1;
  char cVar4;
  uint uVar2;
  ushort uVar3;
  ushort *puVar5;
  uint uVar6;
  undefined *puVar7;
  int iVar8;
  byte bVar9;
  uint *puVar10;
  uint *puVar11;
  undefined1 auStack_20 [8];
  
  puVar7 = PTR_DAT_000113b4;
  puVar1 = PTR_FUN_000113b0;
  bVar9 = *PTR_Startup_AdcAReadinessState_000113ac;
  cVar4 = (*(code *)PTR_FUN_000113b0)(PTR_DAT_000113b4);
  while (cVar4 != '\x01') {
    cVar4 = (*(code *)puVar1)(puVar7);
  }
  uVar2 = (*(code *)PTR_OutputHandoff_ReadAdcCount_000113b8)(puVar7);
  puVar1 = PTR_OutputCycle_ConvertInputB_000113bc;
  *(uint *)(int)DAT_000113a4 = uVar2 & 0xffff;
  uVar3 = (*(code *)puVar1)(uVar2 & 0xffff,auStack_20);
  puVar5 = (ushort *)(int)DAT_0001139c;
  *puVar5 = uVar3;
  puVar7 = PTR_OutputTask_ReadTimestamp_000113c4;
  puVar1 = PTR_LAB_000113c0;
  iVar8 = (int)DAT_000113a8;
  uVar2 = (uint)bVar9;
  puVar10 = (uint *)(int)DAT_0001139e;
  puVar11 = (uint *)(int)DAT_000113a2;
  uVar6 = (uint)*puVar5;
  if (uVar2 == 1) {
    if ((int)uVar6 <= (int)DAT_000113a6) {
      if (iVar8 < (int)uVar6) {
        *puVar10 = 0;
LAB_00011436:
        *puVar11 = 0;
        goto LAB_00011462;
      }
      if (*puVar11 == 0) {
LAB_00011382:
        *puVar10 = 0;
LAB_0001141a:
        uVar2 = (*(code *)puVar7)();
        *puVar11 = uVar2;
        goto LAB_00011462;
      }
      uVar2 = (*(code *)PTR_OutputTask_ReadTimestamp_000113c4)();
      puVar7 = (undefined *)(uVar2 - *puVar11);
      goto joined_r0x00011404;
    }
    if (*puVar10 != 0) {
      uVar2 = (*(code *)PTR_OutputTask_ReadTimestamp_000113c4)();
      puVar7 = (undefined *)(uVar2 - *puVar10);
joined_r0x00011372:
      if (puVar1 <= puVar7) {
        *puVar10 = 0;
        bVar9 = 2;
      }
      goto LAB_00011462;
    }
    *puVar11 = 0;
  }
  else if (uVar2 == 2) {
    puVar10 = (uint *)(int)DAT_00011478;
    if ((int)uVar6 <= (int)DAT_0001147a) {
      if (iVar8 < (int)uVar6) {
        *puVar11 = 0;
        *puVar10 = 0;
        goto LAB_00011462;
      }
      if (*puVar11 == 0) goto LAB_00011382;
      uVar2 = (*(code *)PTR_OutputTask_ReadTimestamp_000113c4)();
      puVar7 = (undefined *)(uVar2 - *puVar11);
      goto joined_r0x00011404;
    }
    if (*puVar10 != 0) {
      uVar2 = (*(code *)PTR_OutputTask_ReadTimestamp_000113c4)();
      if (puVar1 <= (undefined *)(uVar2 - *puVar10)) {
        *puVar10 = 0;
        bVar9 = 3;
      }
      goto LAB_00011462;
    }
    *puVar11 = 0;
  }
  else {
    if (uVar2 == 3) {
      if (iVar8 < (int)uVar6) goto LAB_00011436;
      if (*puVar11 == 0) goto LAB_0001141a;
      uVar2 = (*(code *)PTR_OutputTask_ReadTimestamp_000113c4)();
      puVar7 = (undefined *)(uVar2 - *puVar11);
joined_r0x00011404:
      if (puVar1 <= puVar7) {
        *puVar11 = 0;
        bVar9 = 4;
      }
      goto LAB_00011462;
    }
    if (uVar2 != 4) goto LAB_00011462;
    if ((int)uVar6 <= (int)DAT_000113a6) {
      *puVar10 = 0;
      goto LAB_00011462;
    }
    if (*puVar10 != 0) {
      uVar2 = (*(code *)PTR_OutputTask_ReadTimestamp_000113c4)();
      puVar7 = (undefined *)(uVar2 - *puVar10);
      goto joined_r0x00011372;
    }
  }
  uVar2 = (*(code *)puVar7)();
  *puVar10 = uVar2;
LAB_00011462:
  *PTR_Startup_AdcAReadinessState_0001147c = bVar9;
  return uVar2;
}

