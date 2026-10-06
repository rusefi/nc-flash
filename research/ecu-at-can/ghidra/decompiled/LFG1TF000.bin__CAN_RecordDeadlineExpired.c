/* Ghidra analysis output; verify against original SH instructions. */

/* Unsigned current tick >= stored deadline; equality expires.108 record/slot/boundary cases
   verified. Global wrap policy unresolved. */

bool CAN_RecordDeadlineExpired(byte param_1,byte param_2)

{
  uint uVar1;
  
  uVar1 = (*(code *)PTR_Tick_Read_00019d40)();
  return *(uint *)((int)DAT_00019d3a + (uint)param_1 * 8 + (uint)param_2 * 4) <= uVar1;
}

