/* Ghidra analysis output; verify against original SH instructions. */

/* WARNING: Removing unreachable block (ram,0x00031b94) */
/* WARNING: Removing unreachable block (ram,0x00031bca) */
/* Event2 phase service; completion can drain groups/retire ring through nested event3. Original
   native code0 targetqualification104, groups02/25 ack andretirement108/freeheap; newnaturalcode2
   at113 prevents durableidle. See tcu-phase-retirement.txt andtcu-recovery-reference.txt. */

undefined4 Phase_ServiceRecords(void)

{
  byte bVar1;
  undefined *puVar2;
  char cVar6;
  int iVar3;
  int iVar4;
  undefined2 uVar5;
  int iVar7;
  uint uVar8;
  ushort uVar10;
  int iVar9;
  uint *puVar11;
  undefined1 local_28 [12];
  
  puVar2 = PTR_Phase_RecordRing_00031b84;
  puVar11 = (uint *)local_28;
  for (iVar7 = 0; iVar7 < (int)(uint)(byte)puVar2[DAT_00031c94]; iVar7 = iVar7 + 1) {
    uVar8 = (uint)(byte)puVar2[DAT_00031b80] + iVar7 + 0x10 & 0xf;
    uVar10 = (ushort)uVar8;
    iVar9 = (short)uVar10 * 0xf;
    *puVar11 = (uint)(byte)puVar2[iVar9 + 10];
    puVar11[1] = (uint)(byte)puVar2[iVar9 + 0xb];
    bVar1 = puVar2[iVar9 + 0xc];
    cVar6 = (*(code *)PTR_FUN_00031b88)(uVar8,*puVar11,(uint)bVar1);
    if ((cVar6 == '\x01') || ((*(byte *)(int)DAT_00031b82 & 1) == 1)) {
      *(byte *)(int)DAT_00031b82 = *(byte *)(int)DAT_00031b82 & 0xfe;
      if (uVar10 == (byte)puVar2[DAT_00031b80]) {
        Phase_NotifyRequestGroups(1,uVar8);
        puVar2[iVar9 + 0xd] = 3;
      }
      else {
        bVar1 = puVar2[DAT_00031b80];
        iVar9 = 0;
        if (-1 < iVar7) {
          do {
            uVar8 = (uint)bVar1 + iVar9 + 0x10 & 0xf;
            Phase_NotifyRequestGroups(1,uVar8);
            iVar9 = iVar9 + 1;
            puVar2[(short)uVar8 * 0xf + 0xd] = 3;
          } while (iVar9 <= iVar7);
        }
      }
    }
    else if (puVar2[iVar9 + 0xd] != '\x03') {
      iVar3 = (int)(char)puVar2[iVar9 + 0xd];
      puVar11[-1] = (uint)bVar1;
      iVar4 = (*(code *)PTR_Phase_EvaluateTransitions_00031b8c)(iVar3,uVar8,*puVar11,puVar11[1]);
      if (iVar4 != -1) {
        puVar2[iVar9 + 0xd] = (char)iVar4;
        if ((iVar3 == 0) && (iVar4 < 2)) {
          puVar11[-1] = 0;
          puVar11[-2] = DAT_00031b90;
          puVar11 = puVar11 + -2;
          uVar5 = (*(code *)PTR_FUN_00031c9c)();
          *(undefined2 *)(PTR_Phase_DepartureTimers_00031ca0 + (short)uVar10 * 2) = uVar5;
          (*(code *)PTR_FUN_00031ca4)(uVar8);
        }
        if ((iVar3 < 2) && (iVar4 == 2)) {
          *(undefined4 *)((int)puVar11 + -4) = 0;
          *(undefined4 *)((int)puVar11 + -8) = DAT_00031ca8;
          puVar11 = (uint *)((int)puVar11 + -8);
          uVar5 = (*(code *)PTR_FUN_00031c9c)();
          *(undefined2 *)(PTR_Phase_CompletionTimers_00031cac + (short)uVar10 * 2) = uVar5;
        }
        if ((iVar3 < 3) && (iVar4 == 3)) {
          Phase_NotifyRequestGroups(3,uVar8);
        }
      }
    }
  }
  return 0xffffffff;
}

