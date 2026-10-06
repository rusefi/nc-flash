/* Ghidra analysis output; verify against original SH instructions. */

/* Executed valid handle release, mode clear andA202 decrement; no repeated/invalid release claim.
    */

int SparkRequest_ReleaseFirstListEntry(byte param_1)

{
  int iVar1;
  short *psVar2;
  
  (*(code *)PTR_RequestList_Release_0004c860)
            ((int)(char)param_1,PTR_DAT_0004c85c,PTR_SparkRequest_FirstListDescriptor_0004c858);
  psVar2 = (short *)(int)DAT_0004c848;
  iVar1 = (int)DAT_0004c846;
  *(undefined1 *)((uint)param_1 + iVar1) = 0;
  *psVar2 = *psVar2 + -1;
  return iVar1;
}

