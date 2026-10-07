/* Ghidra analysis output; verify against original SH instructions. */

/* Executed insideoriginal121F8:phase84F4=0,52994,185E4,19794(0),197A6,5327C(0),stage84F5=0. Three
   initializedadmission traces; coverage/selectedstatechecks,notfullindependentRAMoracle.
   tcu-readiness-admission.txt. */

void Task_InitializeApplicationState(void)

{
  undefined *puVar1;
  
  puVar1 = PTR_OutputPins_InitSources_00012768;
  *PTR_Task_ApplicationPhaseCounter_00012764 = 0;
  (*(code *)puVar1)();
  (*(code *)PTR_OutputPins_InitCommand_0001276c)();
  (*(code *)PTR_FUN_00012770)(0);
  (*(code *)PTR_FUN_00012774)(0);
  (*DAT_00012778)();
  *(undefined1 *)(int)DAT_00012762 = 0;
  return;
}

