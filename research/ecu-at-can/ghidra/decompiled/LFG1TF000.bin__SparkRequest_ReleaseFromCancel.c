/* Ghidra analysis output; verify against original SH instructions. */

/* Constructor-table event2 release callback; releases handle andqueues manager completion.
   Fullmanager cancel fromstates2..5 verified. See tcu-request-dispatch.txt. */

undefined4
SparkRequest_ReleaseFromCancel(undefined1 param_1,undefined4 param_2,undefined4 param_3,int param_4)

{
  undefined *puVar1;
  undefined1 *puVar2;
  
  (*(code *)PTR_SparkRequest_ReleaseFirstListEntry_0004ccfc)((int)*(char *)(param_4 + 2));
  puVar2 = (undefined1 *)(*(code *)PTR_EventMessage_NextBuffer_0004cd00)();
  puVar1 = PTR_DAT_00050004_1_0004cd04;
  *puVar2 = param_1;
  (*(code *)PTR_EventQueue_Enqueue_0004cd08)(0,8,puVar1);
  return 1;
}

