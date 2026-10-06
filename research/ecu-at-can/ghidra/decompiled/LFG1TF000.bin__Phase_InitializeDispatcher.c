/* Ghidra analysis output; verify against original SH instructions. */

/* Event0 clears ring head/count and period phase96C6, sets8089FF, returns state1; executed. */

undefined4 Phase_InitializeDispatcher(void)

{
  FUN_00031e9a();
  FUN_00031f5e();
  *(undefined1 *)(int)DAT_00031a4c = 0;
  return 1;
}

