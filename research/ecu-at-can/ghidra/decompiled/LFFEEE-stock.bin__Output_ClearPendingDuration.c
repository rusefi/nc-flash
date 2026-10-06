/* Ghidra analysis output; verify against original SH instructions. */

/* Protected clear of6784+4*channel. Executed after scheduler cancellation; other channels
   preserved. */

void Output_ClearPendingDuration(byte param_1)

{
  undefined4 uVar1;
  
  uVar1 = (*(code *)PTR_FUN_0002f344)(0x10);
  *(undefined4 *)(PTR_Output_PendingDurations_0002f348 + (uint)param_1 * 4) = 0;
  (*(code *)PTR_FUN_0002f34c)(uVar1);
  return;
}

