/* Ghidra analysis output; verify against original SH instructions. */

/* Mode8002 exact3 executes16F78/50B48/16E80/511CC,othersreturn. Fullcallback
   tested;A518nowfirmware-produced in retainedoutputtask. See tcu-cycle-callback.txt. */

uint OutputCycle_UpdateInputs(void)

{
  uint uVar1;
  
  uVar1 = (uint)DAT_ffff8002;
  if ((uVar1 != 1) && (uVar1 == 3)) {
    (*(code *)PTR_OutputCycle_FilterInputA_000124e8)();
    (*(code *)PTR_OutputCycle_PublishInputA_000124ec)();
    (*(code *)PTR_OutputCycle_FilterInputB_000124f0)();
    uVar1 = (*(code *)PTR_OutputCycle_PublishInputB_000124f4)();
    return uVar1;
  }
  return uVar1;
}

