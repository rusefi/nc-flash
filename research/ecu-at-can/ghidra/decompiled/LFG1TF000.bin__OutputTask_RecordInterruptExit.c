/* Ghidra analysis output; verify against original SH instructions. */

/* Unsigned32(timestamp-start)/10 capped65535 to8698+2i,max86BC+2i. Wrap/saturation/retainedmax
   tested; timestampunits open. See tcu-output-task.txt. CaptureISRindices5/6 wrap/saturation/max
   andexactF6C0 reads verified in512 handlerpairs; tcu-capture-interrupts.txt. */

int OutputTask_RecordInterruptExit(byte param_1)

{
  int iVar1;
  undefined *puVar2;
  int iVar3;
  
  iVar1 = (*(code *)PTR_OutputTask_ReadTimestamp_00015c48)();
  puVar2 = (undefined *)
           (*(code *)PTR_FUN_00015c50)(iVar1 - *(int *)((uint)param_1 * 4 + (int)DAT_00015c3c));
  if (PTR_DAT_00015c54 < puVar2) {
    puVar2 = PTR_DAT_00015c54;
  }
  iVar1 = (uint)param_1 * 2;
  if ((undefined *)(uint)*(ushort *)(DAT_00015c42 + iVar1) < puVar2) {
    *(short *)(DAT_00015c42 + iVar1) = (short)puVar2;
  }
  iVar3 = (int)DAT_00015c44;
  *(short *)(iVar1 + iVar3) = (short)puVar2;
  return iVar3;
}

