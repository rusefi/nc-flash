/* Ghidra analysis output; verify against original SH instructions. */

/* Executed unlink then append to free list, restoring sentinel; bank wrapper clears parallel mode.
    */

void RequestList_Release(char param_1,undefined4 param_2,char *param_3)

{
  RequestList_Unlink((int)param_1,param_2);
  RequestList_InsertBeforeHead((int)*param_3,(int)param_1,param_2,(int)*(short *)(param_3 + 2));
  return;
}

