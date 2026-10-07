/* Ghidra analysis output; verify against original SH instructions. */

/* Zero110bytes8910 history,11counts897E,11states898A,index8989.16 fullRAMchecks. See
   tcu-output-task.txt. */

void OutputTask_InitInputHistory(void)

{
  code *pcVar1;
  
  pcVar1 = DAT_00017c08;
  (*DAT_00017c08)((int)DAT_00017bfe,0,0x6e);
  (*pcVar1)((int)DAT_00017c00,0,0xb);
  (*pcVar1)((int)DAT_00017c02,0,0xb);
  *(undefined1 *)(int)DAT_00017c04 = 0;
  return;
}

