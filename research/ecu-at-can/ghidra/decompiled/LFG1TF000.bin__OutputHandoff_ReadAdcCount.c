/* Ghidra analysis output; verify against original SH instructions. */

/* Reads selected pointer word and returns (raw>>6)&1023. Extended full17B1A descriptor scan:8
   ADCaddresses plus three zero-descriptor ROM400 reads yielding316. No hardwarecompletion model;
   see tcu-output-task.txt. */

ushort OutputHandoff_ReadAdcCount(undefined4 *param_1)

{
  return *(ushort *)*param_1 >> 6 & DAT_000141a8;
}

