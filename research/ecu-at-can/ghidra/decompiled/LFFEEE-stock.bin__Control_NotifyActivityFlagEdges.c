/* Ghidra analysis output; verify against original SH instructions. */

/* OriginalDAE8 callbacks:735Eold0/735Bnew1 ->index7/1616C/660E++;old1/new0
   ->index8/16178/660F++;always735E=new. Nonbinarybyteschecked;notperiodictasknotifications.
   control-activity-hooks.txt. */

uint Control_NotifyActivityFlagEdges(void)

{
  char cVar1;
  undefined *puVar2;
  uint uVar3;
  undefined4 auStack_10 [2];
  
  puVar2 = PTR_Control_PreviousActivityFlag_00042d3c;
  cVar1 = *PTR_Control_ActivityFlag_00042d38;
  if ((*PTR_Control_PreviousActivityFlag_00042d3c == '\0') && (cVar1 == '\x01')) {
    auStack_10[0] = 0;
    (*(code *)PTR_Control_DispatchDescriptorEvent_00042d40)(0,7,auStack_10);
  }
  uVar3 = (uint)(byte)*puVar2;
  if ((uVar3 == 1) && (cVar1 == '\0')) {
    auStack_10[0] = 0;
    uVar3 = (*(code *)PTR_Control_DispatchDescriptorEvent_00042d40)(0,8,auStack_10);
  }
  *puVar2 = cVar1;
  return uVar3;
}

