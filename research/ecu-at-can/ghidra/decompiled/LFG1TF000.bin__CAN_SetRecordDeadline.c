/* Ghidra analysis output; verify against original SH instructions. */

/* Stores tick84D0 + record5C610 interval+8/+10 into8B38+8*record+4*slot. Absolute tick duration
   unresolved. */

void CAN_SetRecordDeadline(byte param_1,char param_2)

{
  int iVar1;
  int *piVar2;
  
  iVar1 = (*(code *)PTR_Tick_Read_00019e54)();
  piVar2 = (int *)((uint)param_1 * 8 + (int)DAT_00019e50);
  if (param_2 == '\0') {
    *piVar2 = iVar1 + (uint)*(ushort *)
                             (PTR_CAN_RecordConfiguration_00019e58 + (uint)param_1 * 0x1c + 8);
  }
  else if (param_2 == '\x01') {
    piVar2[1] = iVar1 + (uint)*(ushort *)
                               (PTR_CAN_RecordConfiguration_00019e58 + (uint)param_1 * 0x1c + 10);
  }
  return;
}

