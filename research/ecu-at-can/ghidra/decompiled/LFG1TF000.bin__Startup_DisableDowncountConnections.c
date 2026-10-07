/* Ghidra analysis output; verify against original SH instructions. */

/* 256 originalwholeRAM/register cases: TCNR F662 word0 disables compare-match start connections
   under compatible section11.2.12. Shared strict configuration owner. Full15574 next stops1461A
   wordF430, conflicting with documented TCNT0 long-only width; no forcedflags.
   tcu-downcount-startup.txt. */

void Startup_DisableDowncountConnections(void)

{
  *(undefined2 *)(int)DAT_000146ec = 0;
  return;
}

