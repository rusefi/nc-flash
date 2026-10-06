/* Ghidra analysis output; verify against original SH instructions. */

/* Executed node word setter and parallel mode byte; candidate fixtures and one stock callback
   tested. */

int SparkRequest_SetSecondListEntry(byte param_1,undefined4 param_2,char param_3)

{
  (*(code *)PTR_RequestList_SetValue_0004cb84)((int)(char)param_1,param_2,PTR_DAT_0004cb78);
  *(char *)((uint)param_1 + (int)DAT_0004cb66) = param_3;
  return (int)param_3;
}

