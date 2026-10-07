/* Ghidra analysis output; verify against original SH instructions. */

/* Executed256cases:6605=0,6606=1; otherapplicationRAMunchanged. Notfullboot. */

void Control_InitializeStopState(void)

{
  undefined *puVar1;
  
  puVar1 = PTR_DAT_0002c63c;
  *PTR_Control_StopState_0002c638 = 0;
  *puVar1 = 1;
  return;
}

