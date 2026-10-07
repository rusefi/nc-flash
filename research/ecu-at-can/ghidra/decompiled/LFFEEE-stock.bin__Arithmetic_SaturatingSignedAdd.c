/* Ghidra analysis output; verify against original SH instructions. */

/* Executed100 boundarypairs plus1800 ADDV instructioncases. Signed32 sum clamps at INT_MIN/INT_MAX;
   original2034 executes. control-task-serial.txt. */

int Arithmetic_SaturatingSignedAdd(int param_1,int param_2)

{
  char cVar1;
  
  cVar1 = (param_1 < 0) + (param_2 < 0);
  param_1 = param_2 + param_1;
  if ((cVar1 == '\0' || cVar1 == '\x02') && (char)((param_1 < 0) + (param_2 < 0)) == '\x01') {
    param_1 = DAT_00002048 + (uint)(-1 < param_1);
  }
  return param_1;
}

