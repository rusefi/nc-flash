/* Ghidra analysis output; verify against original SH instructions. */

/* Queue3 tested:descriptor11374
   base49C4/taskindex4/capacity100,45D9tail/45DBcount,20bytefivewordrecord.1536nonempty/full+192empty
   admissions PASS; emptycalls35E0->391A. Unused3argumentwords copied fromcallerstack. Queue2
   additional1488wholeRAM producer cases PASS;48empty/48full; task3priority2.
   Inlinepreemptionnotproved; control-timer-event2.txt. control-queued-event2.txt. */

undefined4 Control_EnqueueCallbackRecord(uint param_1,undefined4 *param_2)

{
  byte bVar1;
  short sVar2;
  undefined *puVar3;
  undefined4 uVar4;
  int *piVar5;
  byte *pbVar6;
  int iVar7;
  undefined4 *puVar8;
  int iVar9;
  undefined4 uVar10;
  
  iVar9 = 0;
  piVar5 = (int *)(PTR_PTR_0000f688 + (param_1 & 0xffff) * 8);
  iVar7 = *piVar5;
  sVar2 = *(short *)(piVar5 + 1);
  bVar1 = *(byte *)((int)piVar5 + 6);
  uVar4 = (*(code *)PTR_FUN_0000f68c)((int)DAT_0000f684);
  puVar3 = PTR_DAT_0000f690;
  if ((byte)PTR_DAT_0000f690[(param_1 & 0xffff) * 3 + 2] < bVar1) {
    if (PTR_DAT_0000f690[(param_1 & 0xffff) * 3 + 2] == '\0') {
      iVar9 = (*(code *)PTR_Control_ActivateTaskFromDescriptor_0000f694)((int)sVar2);
    }
    if (iVar9 == 0) {
      pbVar6 = puVar3 + (param_1 & 0xffff) * 3;
      pbVar6[2] = pbVar6[2] + 1;
      puVar8 = (undefined4 *)(iVar7 + (uint)*pbVar6 * 0x14);
      iVar9 = 5;
      do {
        iVar9 = iVar9 + -1;
        uVar10 = *param_2;
        param_2 = param_2 + 1;
        *puVar8 = uVar10;
        puVar8 = puVar8 + 1;
      } while (iVar9 != 0);
      pbVar6 = puVar3 + (param_1 & 0xffff) * 3;
      *pbVar6 = *pbVar6 + 1;
      uVar10 = 0;
      if (bVar1 <= *pbVar6) {
        puVar3[(param_1 & 0xffff) * 3] = 0;
      }
    }
    else {
      uVar10 = 1;
      (*(code *)PTR_FUN_0000f698)((int)sVar2);
    }
  }
  else {
    uVar10 = 2;
  }
  (*(code *)PTR_FUN_0000f69c)(uVar4);
  return uVar10;
}

