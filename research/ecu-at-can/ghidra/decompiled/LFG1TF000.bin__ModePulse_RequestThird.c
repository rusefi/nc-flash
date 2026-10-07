/* Ghidra analysis output; verify against original SH instructions. */

/* Writes9419=1;23DD0 sets9416=1/resets82BA. See tcu-inhibit-writers.txt. */

void ModePulse_RequestThird(void)

{
  *(undefined1 *)(int)DAT_00023e86 = 1;
  return;
}

