/* Ghidra analysis output; verify against original SH instructions. */

/* Writes bit0 from88B7==1 and bit3 from88B5==1. Table5E98C identifier1709; physical semantics
   unverified. */

int Diagnostic_GetSelectorInputsOneAndThree(int param_1,byte *param_2)

{
  byte bVar1;
  
  bVar1 = *pcRam000555fc == '\x01';
  if (*pcRam00055600 == '\x01') {
    bVar1 = bVar1 | 8;
  }
  *param_2 = bVar1;
  return (int)*(char *)(param_1 + 3);
}

