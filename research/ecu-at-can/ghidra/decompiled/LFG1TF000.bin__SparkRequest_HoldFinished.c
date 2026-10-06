/* Ghidra analysis output; verify against original SH instructions. */

/* Calls4D3D8 and4D7CC with81F2[slot]; true causes4CEF2 then5 ramp callback on same update. See
   tcu-request-dispatch.txt. */

void SparkRequest_HoldFinished(undefined4 param_1,int param_2)

{
  undefined1 uVar1;
  undefined4 uVar2;
  
  uVar1 = PTR_Request_HoldTimerSlots_0004cff0[*(byte *)(param_2 + 0xc)];
  uVar2 = (*(code *)PTR_SparkRequest_SelectHoldDuration_0004cff4)();
  (*(code *)PTR_SparkRequest_CheckHoldTime_0004cff8)(uVar1,uVar2,param_2);
  return;
}

