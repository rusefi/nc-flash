/* Ghidra analysis output; verify against original SH instructions. */

/* Executed indexed node word setter; no general bounds claim. */

void RequestList_SetValue(uint param_1,undefined2 param_2,int param_3)

{
  *(undefined2 *)((param_1 & 0xff) * 4 + param_3 + 2) = param_2;
  return;
}

