/* Ghidra analysis output; verify against original SH instructions. */

/* Writes9418=1;23DD0 sets9415=1/resets82B9. Retainedrequestusesoriginalsetter. See
   tcu-inhibit-writers.txt. */

void ModePulse_RequestSecond(void)

{
  *(undefined1 *)(int)DAT_00023e84 = 1;
  return;
}

