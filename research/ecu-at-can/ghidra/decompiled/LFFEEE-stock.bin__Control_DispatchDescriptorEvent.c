/* Ghidra analysis output; verify against original SH instructions. */

/* WARNING: Type propagation algorithm not settling */
/* Bank0/index4 row1148C selector3/onearg/target2BCE6 nowexecutes F5A0
   queuedbranch.1536nonempty/full+192empty admission wholeRAM cases PASS; directFFFF hookproof
   retained. control-queued-event2.txt; notallbank/selectorproof. */

undefined4 Control_DispatchDescriptorEvent(uint param_1,uint param_2,undefined4 *param_3)

{
  int iVar1;
  undefined4 uVar2;
  ushort *puVar3;
  undefined4 local_24 [6];
  
  puVar3 = (ushort *)(*(int *)(PTR_PTR_0000dc00 + (param_1 & 0xff) * 4) + (param_2 & 0xffff) * 8);
  local_24[0] = *(undefined4 *)(puVar3 + 2);
  for (iVar1 = 1; iVar1 <= (int)(uint)puVar3[1]; iVar1 = iVar1 + 1) {
    uVar2 = *param_3;
    param_3 = param_3 + 1;
    local_24[iVar1] = uVar2;
  }
  uVar2 = 0;
  if ((undefined *)(uint)*puVar3 == PTR_DAT_0000fffc_3_0000dc04) {
    (**(code **)(puVar3 + 2))(local_24 + 1);
  }
  else {
    iVar1 = (*DAT_0000dc08)((int)(short)*puVar3,local_24);
    if (iVar1 != 0) {
      uVar2 = 1;
    }
  }
  return uVar2;
}

