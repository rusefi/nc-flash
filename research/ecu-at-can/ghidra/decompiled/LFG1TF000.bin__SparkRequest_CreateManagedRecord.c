/* Ghidra analysis output; verify against original SH instructions. */

/* Chooses group via4C880,20-byte allocation via2FBEE, appends request ring andqueues constructor
   event. Executed code6/7 group8; outer dispatcher must updateA2B8 state. See
   tcu-request-dispatch.txt. */

undefined4 SparkRequest_CreateManagedRecord(char param_1,short param_2,short param_3,short param_4)

{
  undefined *puVar1;
  undefined *puVar2;
  uint uVar3;
  undefined2 *puVar4;
  undefined4 uVar5;
  
  uVar3 = SparkRequest_SelectManagedGroup((int)param_2,(int)param_3,(int)param_4);
  if ((undefined *)(uVar3 & 0xffff) == PTR_DAT_0004c594) {
    puVar4 = (undefined2 *)(*(code *)PTR_EventMessage_NextBuffer_0004c598)();
    puVar2 = PTR_EventQueue_Enqueue_0004c5a0;
    puVar1 = PTR_DAT_0004c59c;
    *(char *)(puVar4 + 1) = param_1;
    *puVar4 = 5;
    (*(code *)puVar2)(0,5,puVar1);
    uVar5 = 1;
  }
  else {
    uVar5 = (*(code *)PTR_FUN_0004c5a8)(uVar3,PTR_PTR_0004c5a4);
    (*(code *)PTR_RequestManager_AllocateAndQueue_0004c5ac)
              (PTR_DAT_0004c58c,PTR_SparkRequest_ManagerDescriptor_0004c588,(int)param_1,
               (int)param_2,(int)param_3,5,uVar3,1,uVar5);
    uVar5 = 2;
  }
  return uVar5;
}

