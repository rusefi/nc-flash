/* Ghidra analysis output; verify against original SH instructions. */

/* Executed original node value setter and parallel mode byte, full candidate merge/ECU pairing in
   tcu-slot2.txt. */

int SparkRequest_SetFirstListEntry(byte param_1,undefined4 param_2,char param_3)

{
  (*(code *)PTR_RequestList_SetValue_0004c730)((int)(char)param_1,param_2,PTR_DAT_0004c724);
  *(char *)((uint)param_1 + (int)DAT_0004c702) = param_3;
  return (int)param_3;
}

