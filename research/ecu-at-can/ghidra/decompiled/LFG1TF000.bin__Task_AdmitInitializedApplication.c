/* Ghidra analysis output; verify against original SH instructions. */

/* Originalcalls1DFF8 thensets84F5=1. Nativeadmission retainsfullgroupstate;62-callfixturealone
   differs209bytes. Joinednativecapturestartup3traces PASS; no forcedreadyflags/historyreset.
   tcu-native-group-initialization.txt/tcu-native-capture-startup.txt. */

void Task_AdmitInitializedApplication(void)

{
  (*(code *)PTR_Application_InitializeOperationalGroups_0001277c)();
  *(undefined1 *)(int)DAT_00012762 = 1;
  return;
}

