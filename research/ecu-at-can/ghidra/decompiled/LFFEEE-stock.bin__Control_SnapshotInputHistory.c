/* Ghidra analysis output; verify against original SH instructions. */

/* Mode7016zero refreshesprotected8070/8064 from80BC;allmodes snapshotto8084/8088. Original3880/3894
   withnonzero interruptmask;zero-mask scheduler pathopen. */

void Control_SnapshotInputHistory(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined4 uVar3;
  char cVar4;
  undefined4 uVar5;
  
  uVar5 = *(undefined4 *)PTR_Control_BaselineInput_000586e8;
  uVar3 = (*(code *)PTR_FUN_00058704)(0x10);
  cVar4 = (*(code *)PTR_FUN_0005870c)(PTR_DAT_00058708);
  if (cVar4 == '\0') {
    (*(code *)PTR_FUN_000586f4)(uVar5,PTR_Control_ProtectedPriorInputTarget_000586fc);
    (*(code *)PTR_FUN_000586f4)(uVar5,PTR_Control_ProtectedPriorFilteredInput_00058700);
  }
  uVar5 = (*(code *)PTR_FUN_00058710)(PTR_Control_ProtectedPriorInputTarget_000586fc);
  puVar2 = PTR_FUN_00058710;
  puVar1 = PTR_Control_ProtectedPriorFilteredInput_00058700;
  *(undefined4 *)PTR_Control_PriorInputTargetSnapshot_00058714 = uVar5;
  uVar5 = (*(code *)puVar2)(puVar1);
  *(undefined4 *)PTR_Control_PriorFilteredInputSnapshot_00058718 = uVar5;
  (*(code *)PTR_FUN_0005871c)(uVar3);
  return;
}

