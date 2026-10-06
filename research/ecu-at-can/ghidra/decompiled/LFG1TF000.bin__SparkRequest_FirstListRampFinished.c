/* Ghidra analysis output; verify against original SH instructions. */

/* Executed timer8115[record+12]>=4D4CC(record). Includes zero-duration path; no physical duration
   claim. */

bool SparkRequest_FirstListRampFinished(undefined4 param_1,int param_2)

{
  byte bVar1;
  int iVar2;
  
  bVar1 = PTR_Request_RampTimerSlots_0004cffc[*(byte *)(param_2 + 0xc)];
  iVar2 = (*(code *)PTR_SparkRequest_SelectFirstListRampDuration_0004d000)(param_2);
  return iVar2 <= (int)(uint)bVar1;
}

