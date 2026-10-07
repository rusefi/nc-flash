/* Ghidra analysis output; verify against original SH instructions. */

/* 256 originalwholeRAM/register cases: word0 F666 preserves sampled DSTR bits under compatible
   only1-writable semantics.65536 zero-write states PASS; nonzero starts rejected without
   DCNT/reload. No counter/terminate events. tcu-downcount-startup.txt. */

void Startup_DSTRZeroCommand(void)

{
  *(undefined2 *)(int)DAT_000149d6 = 0;
  return;
}

