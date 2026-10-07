/* Ghidra analysis output; verify against original SH instructions. */

/* OrderedF730|=F,F734&=FFAA,F738&=FFF0. Wordreadmodifywrites; PBIR unchanged. See
   tcu-output-pin-switch.txt. */

void OutputPins_SelectGeneralLow(void)

{
  ushort *puVar1;
  
  puVar1 = (ushort *)(int)DAT_000157d8;
  *puVar1 = *puVar1 | 0xf;
  puVar1[2] = puVar1[2] & (ushort)PTR_DAT_000157f0;
  puVar1[4] = puVar1[4] & (ushort)PTR_DAT_000157f4;
  return;
}

