/* Ghidra analysis output; verify against original SH instructions. */

/* 256 original wholeRAM/register/MMIO cases: bytezero ITVRR1 F424, ITVRR2A F426, ITVRR2B F428.
   Compatible SH7055S section11.2.7: disables interval IRQ and ADC triggers; no counter-edge or
   physical admission proof.768 latch roundtrips/16 rejects PASS. Full15574 next stops14978
   wordF666=0; recovery868C/D still0. tcu-interval-startup.txt. */

void Startup_DisableIntervalRequests(void)

{
  *(undefined1 *)(int)DAT_000146e6 = 0;
  *(undefined1 *)(int)DAT_000146e8 = 0;
  *(undefined1 *)(int)DAT_000146ea = 0;
  return;
}

