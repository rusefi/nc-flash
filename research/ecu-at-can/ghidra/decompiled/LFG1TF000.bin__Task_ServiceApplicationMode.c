/* Ghidra analysis output; verify against original SH instructions. */

/* STATIC:11EF2/5329A then8007==1 calls122F4,==3 calls12726, then529AC/185F8. Full probe fails
   closed at hardware1412A. */

void Task_ServiceApplicationMode(void)

{
  (*(code *)PTR_FUN_00012780)();
  (*(code *)PTR_Diagnostic_SelectActiveOutput_00012784)();
  if (DAT_ffff8007 == '\x01') {
    (*(code *)PTR_FUN_00012788)();
  }
  else if (DAT_ffff8007 == '\x03') {
    Task_DispatchApplicationPhase();
  }
  (*(code *)PTR_FUN_0001278c)();
  (*(code *)PTR_FUN_00012790)();
  return;
}

