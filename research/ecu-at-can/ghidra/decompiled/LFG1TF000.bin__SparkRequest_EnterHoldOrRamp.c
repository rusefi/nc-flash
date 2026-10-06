/* Ghidra analysis output; verify against original SH instructions. */

/* Clears81F2[slot], evaluateshold atelapsed0; returns4 ifpending,else captures+4
   to+6,clears8115[slot] andreturns5. Verified both paths. See tcu-request-dispatch.txt. */

undefined4 SparkRequest_EnterHoldOrRamp(undefined4 param_1,int param_2)

{
  undefined *puVar1;
  undefined4 uVar2;
  short sVar3;
  
  puVar1 = PTR_SparkRequest_SelectHoldDuration_0004cff4;
  PTR_Request_HoldTimerSlots_0004cff0[*(byte *)(param_2 + 0xc)] = 0;
  uVar2 = (*(code *)puVar1)(param_2);
  sVar3 = (*(code *)PTR_SparkRequest_CheckHoldTime_0004cff8)(0,uVar2,param_2);
  puVar1 = PTR_Request_RampTimerSlots_0004cffc;
  uVar2 = 4;
  if (sVar3 == 1) {
    uVar2 = 5;
    *(undefined2 *)(param_2 + 6) = *(undefined2 *)(param_2 + 4);
    puVar1[*(byte *)(param_2 + 0xc)] = 0;
  }
  return uVar2;
}

