/* Ghidra analysis output; verify against original SH instructions. */

/* Writes9417=1; consumedby23DD0 toone-call9414. See tcu-inhibit-writers.txt. */

void ModePulse_RequestFirst(void)

{
  *(undefined1 *)(int)DAT_00023e82 = 1;
  return;
}

