/* Ghidra analysis output; verify against original SH instructions. */

/* Original1267C tailinitializer executes;565F0 setsA9361,56AD8 clearsgates/states2. Individualinit
   execution isnotfullboot. See tcu-qualified-receive.txt. */

void Diagnostic_InitializeTaskState(void)

{
  (*(code *)PTR_FUN_00056f08)();
  FUN_00056dbe();
  (*(code *)PTR_FUN_00056f0c)();
  (*(code *)PTR_FUN_00056f10)();
  (*(code *)PTR_FUN_00056f14)();
  (*(code *)PTR_FUN_00056f18)();
  (*(code *)PTR_FUN_00056f1c)();
  (*(code *)PTR_FUN_00056f20)();
  (*(code *)PTR_FUN_00056f24)();
  (*(code *)PTR_FUN_00056f28)();
  (*(code *)PTR_FUN_00056f2c)();
  (*(code *)PTR_FUN_00056f30)();
  (*(code *)PTR_FUN_00056f34)();
  (*(code *)PTR_FUN_00056f38)();
  (*(code *)PTR_FUN_00056f3c)();
  (*(code *)PTR_Selector_InitializeDiagnosticTimers_00056f40)();
  (*(code *)PTR_FUN_00056f44)();
  (*(code *)PTR_FUN_00056f48)();
  (*(code *)PTR_FUN_00056f4c)();
  (*(code *)PTR_FUN_00056f50)();
  (*(code *)PTR_FUN_00056f54)();
                    /* WARNING: Could not recover jumptable at 0x00056d60. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*(code *)PTR_LAB_00056f58)();
  return;
}

