/* Ghidra analysis output; verify against original SH instructions. */

/* 11 descriptors5F7B0; fivewordhistories, sharedindexmod5,count/statequalification. Zero
   descriptors5..7 readROM0->400 word4F22 ->316, not sensorinputs.200cases andretainedtask. See
   tcu-output-task.txt. */

void OutputTask_ScanInputHistory(void)

{
  undefined2 uVar1;
  undefined1 *puVar2;
  int iVar3;
  undefined2 *puVar4;
  byte *pbVar5;
  undefined1 *puVar6;
  byte *pbVar7;
  byte *pbVar8;
  int iVar9;
  
  iVar9 = 0;
  puVar2 = (undefined1 *)(int)DAT_00017c02;
  pbVar8 = (byte *)(int)DAT_00017c00;
  pbVar5 = (byte *)(int)DAT_00017c04;
  puVar6 = puVar2;
  pbVar7 = pbVar8;
  do {
    uVar1 = (*(code *)PTR_OutputHandoff_ReadAdcCount_00017c10)
                      (*(undefined4 *)(PTR_PTR_00017c0c + iVar9 * 4));
    puVar4 = (undefined2 *)(iVar9 * 10 + (int)DAT_00017bfe);
    if (pbVar8[iVar9] == 0) {
      iVar3 = 0;
      do {
        iVar3 = iVar3 + 1;
        *puVar4 = uVar1;
        puVar4 = puVar4 + 1;
      } while (iVar3 < 5);
    }
    else {
      puVar4[*pbVar5] = uVar1;
    }
    if (*(char *)(iVar9 + DAT_00017c02) != '\x02') {
      pbVar8[iVar9] = pbVar8[iVar9] + 1;
    }
    iVar9 = iVar9 + 1;
    if (*pbVar7 < 5) {
      *puVar2 = 3;
    }
    else {
      *puVar6 = 2;
    }
    puVar2 = puVar2 + 1;
    puVar6 = puVar6 + 1;
    pbVar7 = pbVar7 + 1;
  } while (iVar9 < 0xb);
  *pbVar5 = *pbVar5 + 1;
  if (4 < *pbVar5) {
    *pbVar5 = 0;
  }
  return;
}

