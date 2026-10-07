/* Ghidra analysis output; verify against original SH instructions. */

/* Event2 pending652D<10 increments beforeDAE8bank0/index4; >=10rejects.1536cases+192emptyqueuecases
   PASS. Pendingincrements evenwhenqueuefull. Event1/otherpaths staticnotnewlyverified.
   control-queued-event2.txt. */

int Control_EnqueueLimitedEvent(int param_1)

{
  undefined *puVar1;
  undefined *puVar2;
  uint uVar3;
  int iVar4;
  byte *pbVar5;
  
  iVar4 = 1;
  if (param_1 == 1) {
    uVar3 = 0;
  }
  else if (param_1 == 2) {
    uVar3 = 1;
  }
  else {
    uVar3 = 2;
  }
  if (uVar3 < 2) {
    pbVar5 = PTR_DAT_0002bdfc + uVar3;
    if (*pbVar5 < 10) {
      *pbVar5 = *pbVar5 + 1;
    }
    else {
      iVar4 = 0;
    }
  }
  puVar2 = PTR_Control_DispatchDescriptorEvent_0002be04;
  puVar1 = PTR_DAT_0002be00;
  if (iVar4 == 1) {
    *(int *)PTR_DAT_0002be00 = param_1;
    iVar4 = (*(code *)puVar2)(0,4,puVar1);
    return iVar4;
  }
  return iVar4;
}

