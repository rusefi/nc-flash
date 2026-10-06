/* Ghidra analysis output; verify against original SH instructions. */

/* Advances96C6 modulo8; filters ten records5D3BC by class5D420; queues op2 and fully drains queue0
   per group. Group5 at even phases. */

undefined4 Request_ServicePeriodicGroups(void)

{
  undefined *puVar1;
  undefined *puVar2;
  byte *pbVar3;
  undefined *puVar4;
  ushort *puVar5;
  undefined *puVar6;
  
  pbVar3 = (byte *)(int)DAT_00031eac;
  *pbVar3 = *pbVar3 + 1;
  if (7 < *pbVar3) {
    *pbVar3 = 0;
  }
  puVar2 = PTR_EventQueue_Enqueue_00031eb8;
  puVar1 = PTR_EventQueue_Drain_00031eb4;
  puVar4 = PTR_Request_PeriodicGroupRecords_00031eb0 + 0x28;
  puVar5 = (ushort *)PTR_Request_PeriodicGroupRecords_00031eb0;
  puVar6 = PTR_Request_PeriodicGroupRecords_00031eb0;
  do {
    if ((puVar6[3] == '\x01') ||
       (puVar6[3] == PTR_Request_PeriodClassTable_00031ebc[*(char *)(int)DAT_00031eac])) {
      (*(code *)puVar2)(0,1,(uint)*puVar5 << 0x10 | 2);
      (*(code *)puVar1)(0);
    }
    puVar6 = puVar6 + 4;
    puVar5 = puVar5 + 2;
  } while (puVar6 < puVar4);
  return 0xffffffff;
}

