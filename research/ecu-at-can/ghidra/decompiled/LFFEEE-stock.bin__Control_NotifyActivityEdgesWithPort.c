/* Ghidra analysis output; verify against original SH instructions. */

/* Sameedgecallbacks as42C68; additionallyPFDRbit3set whenever735Bexact1,includingnoedge.
   4096combinedcases,exactMMIO/fullRAM checked. Pinroleunproved. */

uint Control_NotifyActivityEdgesWithPort(void)

{
  char cVar1;
  undefined *puVar2;
  uint uVar3;
  undefined4 local_18;
  undefined4 auStack_14 [2];
  
  puVar2 = PTR_Control_PreviousActivityFlag_00042d3c;
  cVar1 = *PTR_Control_ActivityFlag_00042d38;
  if (cVar1 == '\x01') {
    (*(code *)PTR_FUN_00042d44)(auStack_14,(int)DAT_00042d34);
    (*(code *)PTR_Register_UpdateMaskedWord_00042d48)((int)DAT_00042d36,8,1);
    (*(code *)PTR_FUN_00042d4c)(auStack_14[0]);
    if (*puVar2 == '\0') {
      local_18 = 0;
      (*(code *)PTR_Control_DispatchDescriptorEvent_00042d40)(0,7,&local_18);
    }
  }
  uVar3 = (uint)(byte)*puVar2;
  if ((uVar3 == 1) && (cVar1 == '\0')) {
    local_18 = 0;
    uVar3 = (*(code *)PTR_Control_DispatchDescriptorEvent_00042d40)(0,8,&local_18);
  }
  *puVar2 = cVar1;
  return uVar3;
}

