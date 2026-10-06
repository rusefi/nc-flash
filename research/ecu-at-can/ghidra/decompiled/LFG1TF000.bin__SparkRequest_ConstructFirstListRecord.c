/* Ghidra analysis output; verify against original SH instructions. */

/* WARNING: Removing unreachable block (ram,0x0004cbcc) */
/* Executed constructor: snapshot808C/80C2/80C4 into+13/+14/+16;2FBA4 event lookup gives timer
   index+12;allocate first-list handle+2,zero+4/+6,return2. Explicit ring fixture; dispatch
   reachability open. See tcu-request-maps.txt. */

undefined4
SparkRequest_ConstructFirstListRecord
          (undefined4 param_1,undefined1 param_2,undefined1 param_3,int param_4)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined2 uVar3;
  undefined1 uVar4;
  int iVar5;
  undefined1 uStack_1c;
  
  *(undefined1 *)(param_4 + 1) = param_2;
  iVar5 = 1;
  *(undefined1 *)(param_4 + 8) = param_3;
  uVar3 = (*(code *)PTR_FUN_0004cce8)();
  *(undefined2 *)(param_4 + 4) = uVar3;
  if (iVar5 == 0) {
    uStack_1c = (char)((uint)DAT_0004cce4 >> 0x18);
  }
  else {
    uStack_1c = (char)((uint)DAT_0004cce0 >> 0x18);
  }
  uVar3 = (*(code *)PTR_FUN_0004cce8)();
  puVar2 = PTR_DAT_0004ccf0;
  puVar1 = PTR_SparkRequest_ManagerDescriptor_0004ccec;
  *(undefined2 *)(param_4 + 6) = uVar3;
  uVar4 = (*(code *)PTR_CallbackQueue_FindEventIndex_0004ccf4)(puVar2,puVar1,(int)uStack_1c);
  *(undefined1 *)(param_4 + 0xc) = uVar4;
  *(undefined1 *)(param_4 + 0xd) = DAT_ffff808c;
  *(undefined2 *)(param_4 + 0xe) = Request_CapturedSourceAxisRaw;
  *(undefined2 *)(param_4 + 0x10) = Request_CapturedSourceAxisScaled;
  uVar4 = (*(code *)PTR_SparkRequest_AllocateFirstList_0004ccf8)(1);
  *(undefined1 *)(param_4 + 2) = uVar4;
  return 2;
}

