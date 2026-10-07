/* Ghidra analysis output; verify against original SH instructions. */

/* Copiesmax(0,s16(92E4)) andraw92F6 into two worddestinations; executedwithinindependent3AC70
   model. */

void ClassBase_CopyRawAxes(short *param_1,undefined2 *param_2)

{
  short sVar1;
  
  sVar1 = *DAT_0003af2c;
  if (sVar1 < 0) {
    sVar1 = 0;
  }
  *param_1 = sVar1;
  *param_2 = *(undefined2 *)PTR_DAT_0003af30;
  return;
}

