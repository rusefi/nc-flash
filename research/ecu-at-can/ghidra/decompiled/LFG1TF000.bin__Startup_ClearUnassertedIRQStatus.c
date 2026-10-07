/* Ghidra analysis output; verify against original SH instructions. */

/* 64 original wholeRAM/register cases:RTSdelay-slot14430 writes0 toISR ED1A. Explicit constantzero
   status/no pending flags or pin assertions; not general read-one/write-zero withdrawal. Full15574
   then stopsUBARH EC00. tcu-icr-startup.txt. */

void Startup_ClearUnassertedIRQStatus(void)

{
  *(undefined2 *)(int)DAT_00014510 = 0;
  return;
}

