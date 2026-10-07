/* Ghidra analysis output; verify against original SH instructions. */

/* 256originalcases PASS:stopboth
   F710=0,readF718,writeC0,compareF71C=2499,counterF71A=0,startF710=2. CompatibleSH7058 CKS0=Pphi/8
   ->20000phi/tick,100000phi/event2request. No absoluteclock/resetreachability/hardwareIRQproof.
   control-timer-event2.txt. */

void Control_InitializeCmt1(void)

{
  undefined2 *puVar1;
  
  puVar1 = (undefined2 *)(int)DAT_000106ac;
  *puVar1 = 0;
  *(undefined2 *)(int)DAT_000106ae = DAT_000106b0;
  *(undefined2 *)(int)DAT_000106b4 = DAT_000106b2;
  *(undefined2 *)(int)DAT_000106b6 = 0;
  *puVar1 = 2;
  return;
}

