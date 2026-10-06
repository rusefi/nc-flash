/* Ghidra analysis output; verify against original SH instructions. */

/* Executed real20-byte heap allocation, constructor message and2FAA2 ring append; no fabricated
   callback record in dispatch lifecycle. See tcu-request-dispatch.txt. */

void RequestManager_AllocateAndQueue
               (undefined4 param_1,undefined4 param_2,char param_3,short param_4,undefined1 param_5,
               short param_6,ushort param_7,short param_8,short param_9)

{
  undefined *puVar1;
  int *piVar2;
  int iVar3;
  undefined1 uStack_1b;
  
  iVar3 = 0;
  if (0 < param_9) {
    iVar3 = (*(code *)PTR_Heap_AllocateRequestStorage_0002fdd8)((int)param_9);
  }
  if ((param_9 == 0) || (iVar3 != 0)) {
    piVar2 = (int *)(*(code *)PTR_EventMessage_NextBuffer_0002fddc)();
    puVar1 = PTR_EventQueue_Enqueue_0002fde0;
    *(char *)(piVar2 + 1) = param_3;
    uStack_1b = (undefined1)param_4;
    *(undefined1 *)((int)piVar2 + 5) = uStack_1b;
    *(undefined1 *)((int)piVar2 + 6) = param_5;
    *piVar2 = iVar3;
    (*(code *)puVar1)(0,(int)param_6,(uint)param_7 << 0x10 | 1);
    RequestManager_AppendRing
              (param_1,param_2,(int)param_3,(int)param_4,(int)(short)param_7,(int)param_8,iVar3);
  }
  return;
}

