/* Ghidra analysis output; verify against original SH instructions. */

/* Completion releases list handle andqueues manager event5; no finalzero numeric update. Fullqueue
   cleanup frees andzerosrecord. See tcu-request-dispatch.txt. */

undefined4 SparkRequest_ReleaseAfterRamp(undefined1 param_1,int param_2)

{
  undefined *puVar1;
  undefined1 *puVar2;
  
  (*(code *)PTR_SparkRequest_ReleaseFirstListEntry_0004d004)((int)*(char *)(param_2 + 2));
  puVar2 = (undefined1 *)(*(code *)PTR_EventMessage_NextBuffer_0004cfdc)();
  puVar1 = PTR_DAT_00050004_1_0004d008;
  *puVar2 = param_1;
  (*(code *)PTR_EventQueue_Enqueue_0004cfe4)(0,8,puVar1);
  return 1;
}

