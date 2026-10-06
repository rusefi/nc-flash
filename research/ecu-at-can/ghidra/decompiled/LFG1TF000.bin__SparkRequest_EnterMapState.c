/* Ghidra analysis output; verify against original SH instructions. */

/* Executes4D7EC flag snapshot andreturns3; manager state3 mayqueue extra operation-change
   notification. Tested managerstate2 entry; additional notification branch open. See
   tcu-request-dispatch.txt. */

undefined4 SparkRequest_EnterMapState(undefined1 param_1,int param_2)

{
  undefined *puVar1;
  undefined *puVar2;
  char cVar4;
  undefined2 *puVar3;
  
  cVar4 = (*(code *)PTR_FUN_0004cfcc)();
  puVar1 = PTR_DAT_0004cfd0;
  (*(code *)PTR_SparkRequest_CaptureSpecialFlag_0004cfd4)(param_2);
  if ((*PTR_DAT_0004cfd8 == '\x03') && (puVar1[cVar4 * 0xc + 7] != *(char *)(param_2 + 1))) {
    puVar3 = (undefined2 *)(*(code *)PTR_EventMessage_NextBuffer_0004cfdc)();
    puVar1 = PTR_DAT_0004cfe0;
    *puVar3 = 8;
    *(undefined1 *)(puVar3 + 1) = param_1;
    puVar2 = PTR_EventQueue_Enqueue_0004cfe4;
    *(undefined1 *)((int)puVar3 + 3) = 3;
    (*(code *)puVar2)(0,8,puVar1);
  }
  return 3;
}

