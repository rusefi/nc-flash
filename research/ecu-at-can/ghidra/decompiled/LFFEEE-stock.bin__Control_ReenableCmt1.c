/* Ghidra analysis output; verify against original SH instructions. */

/* 256originalcases PASS: F710=2,F718=C0,F71C=2499 withoutcounterreset. BackgroundE030/E048
   staticcaller; noCMFsideeffect orhardwareadmissionmodel. control-timer-event2.txt. */

void Control_ReenableCmt1(void)

{
  *(undefined2 *)(int)DAT_000106ac = 2;
  *(undefined2 *)(int)DAT_000106ae = DAT_000106b0;
  *(undefined2 *)(int)DAT_000106b4 = DAT_000106b2;
  return;
}

