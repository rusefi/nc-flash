/* Ghidra analysis output; verify against original SH instructions. */

/* F730=80FF,F732=00A5,F734=0055,F738=0500. SelectsPB0..3 TO6A..D by compatiblemanual; F736
   inversion untouched. See tcu-timer-configuration.txt. */

void TimerSetup_SelectPortBOutputs(void)

{
  *(short *)(int)DAT_00014884 = (short)PTR_DAT_000148c4;
  *(undefined2 *)(int)DAT_00014888 = DAT_00014886;
  *(undefined2 *)(int)DAT_0001488a = 0x55;
  *(undefined2 *)(int)DAT_0001488e = DAT_0001488c;
  return;
}

