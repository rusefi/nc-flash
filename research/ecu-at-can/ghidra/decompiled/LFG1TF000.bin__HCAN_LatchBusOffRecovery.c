/* Ghidra analysis output; verify against original SH instructions. */

/* Called by1B3E8 whenGSRbusoff; disables application communication flags, requests MCRhalt
   through199E0(1), sets8BCF=1.128 handler-body fixtures. */

void HCAN_LatchBusOffRecovery(void)

{
  (*(code *)PTR_FUN_0001ad6c)();
  (*(code *)PTR_FUN_0001ad70)();
  (*(code *)PTR_FUN_0001ad74)();
  (*(code *)PTR_HCAN_SetHaltRequest_0001ad78)(1);
  *(undefined1 *)(int)DAT_0001ad60 = 1;
  return;
}

