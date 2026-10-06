/* Ghidra analysis output; verify against original SH instructions. */

/* Executed valid handle release, mode clear andA258 decrement, queue recycling verified. */

int SparkRequest_ReleaseSecondListEntry(byte param_1)

{
  int iVar1;
  short *psVar2;
  
  (*(code *)PTR_RequestList_Release_0004cb88)
            ((int)(char)param_1,PTR_DAT_0004cb78,PTR_SparkRequest_SecondListDescriptor_0004cb74);
  psVar2 = (short *)(int)DAT_0004cb68;
  iVar1 = (int)DAT_0004cb66;
  *(undefined1 *)((uint)param_1 + iVar1) = 0;
  *psVar2 = *psVar2 + -1;
  return iVar1;
}

