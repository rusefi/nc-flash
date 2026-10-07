/* Ghidra analysis output; verify against original SH instructions. */

/* Originalfull121F8 executes126AC,set8007=1,16A3C timer setup. Three retainedstartup traces
   reachmode3 withoutforcedreadiness; selectedstates/exact6MMIO
   assertions,notcompleteinitializerRAMmodel/fullboot. tcu-readiness-admission.txt. */

void Task_InitializeApplicationAndTimer(void)

{
  (*(code *)PTR_Task_InitializeApplicationState_00012250)();
  DAT_ffff8007 = 1;
  (*DAT_00012254)();
  return;
}

