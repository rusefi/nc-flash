/* Ghidra analysis output; verify against original SH instructions. */

/* One-based channel: original18A44 correction/write then clears selected8A64 sample sum. Full
   original12826 caller tail executed; see tcu-output-handoff.txt. */

void OutputHandoff_ServiceChannel(uint param_1)

{
  int iVar1;
  
  iVar1 = (param_1 & 0xff) - 1;
  OutputHandoff_CorrectAndWrite(iVar1);
  *(undefined2 *)(iVar1 * 2 + (int)DAT_00018870) = 0;
  return;
}

