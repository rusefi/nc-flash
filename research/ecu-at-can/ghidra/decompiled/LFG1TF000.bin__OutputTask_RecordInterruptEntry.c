/* Ghidra analysis output; verify against original SH instructions. */

/* F6C0 timestamp to8728+4i. Stockindex10 scale1: u16latency/10 to86E0+2i,max8704+2i.
   Nestedoriginalhelper executed. See tcu-output-task.txt. CaptureISRindices5/6 stockscale0
   onlystorestart, verified512 handlerpairs; tcu-capture-interrupts.txt. */

void OutputTask_RecordInterruptEntry(byte param_1)

{
  undefined4 uVar1;
  undefined *puVar2;
  int iVar3;
  
  iVar3 = (int)DAT_00015c3c;
  uVar1 = (*(code *)PTR_OutputTask_ReadTimestamp_00015c48)();
  *(undefined4 *)(iVar3 + (uint)param_1 * 4) = uVar1;
  if (*(int *)(PTR_DAT_00015c4c + (uint)param_1 * 4) != 0) {
    puVar2 = (undefined *)(*(code *)PTR_FUN_00015c50)();
    if (PTR_DAT_00015c54 < puVar2) {
      puVar2 = PTR_DAT_00015c54;
    }
    iVar3 = (uint)param_1 * 2;
    if ((undefined *)(uint)*(ushort *)(DAT_00015c3e + iVar3) < puVar2) {
      *(short *)(DAT_00015c3e + iVar3) = (short)puVar2;
    }
    *(short *)(iVar3 + DAT_00015c40) = (short)puVar2;
  }
  return;
}

