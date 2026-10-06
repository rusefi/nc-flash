/* Ghidra analysis output; verify against original SH instructions. */

/* Returns u8ROM76DE0<<12;stock18*4096=73728. Shared ingestion cap/history default. See
   tcu-measurement.txt. */

int Measurement_ReadResetPeriod(void)

{
  return (uint)(byte)*PTR_DAT_000214ec << 0xc;
}

