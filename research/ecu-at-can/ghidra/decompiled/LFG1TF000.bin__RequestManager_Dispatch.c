/* Ghidra analysis output; verify against original SH instructions. */

/* Generic manager executed using stock first-list descriptor. Event2 schedules group8 update
   callbacks; completion/cancel removes ring entries andfrees allocated record. Other
   descriptors/concurrency unverified. See tcu-request-dispatch.txt. */

void RequestManager_Dispatch(short param_1,short *param_2,char *param_3,int *param_4)

{
  char cVar1;
  char cVar2;
  undefined *puVar3;
  code *pcVar4;
  undefined *puVar5;
  undefined *puVar6;
  short sVar9;
  undefined4 *puVar7;
  char cVar11;
  undefined2 *puVar8;
  short sVar10;
  short sVar13;
  int iVar12;
  uint uVar14;
  byte bVar15;
  int iVar16;
  int local_2c;
  
  puVar6 = PTR_EventQueue_Enqueue_0002f874;
  puVar5 = PTR_EventMessage_NextBuffer_0002f870;
  sVar10 = -1;
  if (param_1 == 0) {
    sVar10 = 1;
    param_3[1] = '\0';
    param_3[2] = '\0';
  }
  else if (param_1 == 1) {
    iVar16 = (int)*(char *)param_2;
    uVar14 = (uint)(byte)*param_2;
    cVar1 = *(char *)(param_2 + 1);
    cVar2 = *(char *)((int)param_2 + 3);
    cVar11 = *param_3;
    iVar12 = uVar14 * 4;
    if (cVar11 == '\x01') {
      if ((uVar14 < 0xc) && (*(int *)(uVar14 * 4 + param_4[1]) != 0)) {
        sVar10 = (**(code **)(iVar12 + param_4[1]))(iVar16,uVar14,cVar1,cVar2);
      }
    }
    else if (cVar11 == '\x02') {
      if ((uVar14 < 0xc) && (*(int *)(iVar12 + param_4[2]) != 0)) {
        sVar10 = (**(code **)(iVar12 + param_4[2]))(iVar16,uVar14,cVar1,cVar2);
      }
    }
    else if ((cVar11 == '\x03') && (*(int *)param_4[3] != 0)) {
      sVar10 = (**(code **)param_4[3])(iVar16,uVar14,cVar1,cVar2);
    }
  }
  else if (param_1 == 2) {
    param_3[3] = param_3[3] + '\x01';
    if (7 < (byte)param_3[3]) {
      param_3[3] = '\0';
    }
    for (local_2c = 0; local_2c < (int)(uint)(byte)param_3[2]; local_2c = local_2c + 1) {
      sVar9 = (*(code *)PTR_FUN_0002f878)();
      if (*(char *)(sVar9 * 0xc + *param_4 + 8) == '\x01') {
        bVar15 = 0;
        for (sVar13 = 0; sVar13 < (short)(ushort)*(byte *)((int)param_4 + 0x1b); sVar13 = sVar13 + 1
            ) {
          if (*(short *)(param_4[5] + sVar13 * 4) == *(short *)(*param_4 + sVar9 * 0xc + 4)) {
            bVar15 = *(byte *)(param_4[5] + sVar13 * 4 + 2);
            break;
          }
        }
        if ((bVar15 < 2) || (bVar15 == PTR_DAT_0002f87c[(byte)param_3[3]])) {
          puVar7 = (undefined4 *)(*(code *)puVar5)();
          iVar12 = sVar9 * 0xc;
          *(undefined1 *)(puVar7 + 1) = *(undefined1 *)(iVar12 + *param_4 + 6);
          *puVar7 = *(undefined4 *)(*param_4 + iVar12);
          (*(code *)puVar6)(0,(int)*(short *)(param_4 + 6),
                            (uint)*(ushort *)(*param_4 + iVar12 + 4) << 0x10 | 4);
        }
      }
    }
  }
  else if (param_1 == 3) {
    uVar14 = (uint)*(char *)param_2;
    if ((*param_3 == '\x02') || (*param_3 == '\x03')) {
      for (iVar12 = 0; iVar12 < (int)(uint)(byte)param_3[2]; iVar12 = iVar12 + 1) {
        sVar9 = (*(code *)PTR_FUN_0002f878)();
        if ((uint)*(byte *)(sVar9 * 0xc + *param_4 + 6) == (uVar14 & 0xff)) {
          if (*(char *)(sVar9 * 0xc + *param_4 + 8) != '\x02') {
            puVar7 = (undefined4 *)(*(code *)puVar5)();
            iVar12 = sVar9 * 0xc;
            *(undefined1 *)(puVar7 + 1) = *(undefined1 *)(*param_4 + iVar12 + 6);
            *(undefined1 *)((int)puVar7 + 5) = *(undefined1 *)(*param_4 + iVar12 + 7);
            *puVar7 = *(undefined4 *)(*param_4 + iVar12);
            (*(code *)puVar6)(0,(int)*(short *)(param_4 + 6),
                              (uint)*(ushort *)(*param_4 + iVar12 + 4) << 0x10 | 2);
          }
          break;
        }
      }
    }
  }
  else if (param_1 == 4) {
    if (*param_3 == '\x03') {
      for (iVar12 = 0; iVar12 < (int)(uint)*(byte *)((int)param_4 + 0x1a); iVar12 = iVar12 + 1) {
        iVar16 = iVar12 * 8;
        if ((*param_2 == *(short *)(param_4[4] + iVar16)) &&
           (*(int *)(param_4[4] + iVar16 + 4) != 0)) {
          (**(code **)(param_4[4] + iVar16 + 4))
                    ((int)*(char *)(param_2 + 1),*(char *)((int)param_2 + 3));
          break;
        }
      }
    }
  }
  else if (param_1 == 5) {
    uVar14 = (uint)*(char *)param_2;
    if ((*param_3 == '\x02') || (*param_3 == '\x03')) {
      for (iVar12 = 0; puVar3 = PTR_DAT_0002fb20,
          pcVar4 = (code *)PTR_Heap_ReleaseRequestStorage_0002fb1c,
          iVar12 < (int)(uint)(byte)param_3[2]; iVar12 = iVar12 + 1) {
        sVar10 = (*(code *)PTR_FUN_0002fb18)();
        if ((uint)*(byte *)(*param_4 + sVar10 * 0xc + 6) == (uVar14 & 0xff)) {
          *(undefined1 *)(sVar10 * 0xc + *param_4 + 8) = 2;
          puVar3 = PTR_DAT_0002fb20;
          pcVar4 = (code *)PTR_Heap_ReleaseRequestStorage_0002fb1c;
          break;
        }
      }
      while ((param_3[2] != '\0' &&
             (*(char *)((uint)(byte)param_3[1] * 0xc + *param_4 + 8) == '\x02'))) {
        puVar8 = (undefined2 *)(*(code *)puVar5)();
        *(undefined1 *)(puVar8 + 1) = *(undefined1 *)((uint)(byte)param_3[1] * 0xc + *param_4 + 6);
        *puVar8 = *(undefined2 *)(param_4 + 6);
        (*(code *)puVar6)(0,(int)*(short *)(param_4 + 6),puVar3);
        if (*(int *)((uint)(byte)param_3[1] * 0xc + *param_4) != 0) {
          (*pcVar4)(*(undefined4 *)(*param_4 + (uint)(byte)param_3[1] * 0xc));
        }
        cVar11 = (*(code *)PTR_FUN_0002fb18)();
        param_3[1] = cVar11;
        param_3[2] = param_3[2] + -1;
      }
      while ((param_3[2] != '\0' &&
             (sVar10 = (*(code *)PTR_FUN_0002fb18)(),
             *(char *)(sVar10 * 0xc + *param_4 + 8) == '\x02'))) {
        puVar8 = (undefined2 *)(*(code *)puVar5)();
        *(undefined1 *)(puVar8 + 1) = *(undefined1 *)(sVar10 * 0xc + *param_4 + 6);
        *puVar8 = *(undefined2 *)(param_4 + 6);
        (*(code *)puVar6)(0,(int)*(short *)(param_4 + 6),puVar3);
        if (*(int *)(sVar10 * 0xc + *param_4) != 0) {
          (*pcVar4)(*(undefined4 *)(*param_4 + sVar10 * 0xc));
        }
        param_3[2] = param_3[2] + -1;
      }
      if (param_3[2] == '\0') {
        sVar10 = 1;
      }
      else {
        if (*(char *)((uint)(byte)param_3[1] * 0xc + *param_4 + 8) == '\0') {
          *(undefined1 *)((uint)(byte)param_3[1] * 0xc + *param_4 + 8) = 1;
        }
        if (param_3[2] == '\x01') {
          sVar10 = 2;
        }
        else {
          sVar10 = 3;
        }
      }
    }
  }
  if (sVar10 != -1) {
    *param_3 = (char)sVar10;
  }
  return;
}

