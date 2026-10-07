/* Ghidra analysis output; verify against original SH instructions. */

/* OrderedF738&=FFF0,F730|=F,F734|=55. Wordreadmodifywrites; no electricalpinproof. See
   tcu-output-pin-switch.txt. */

void OutputPins_SelectTimerOutputs(void)

{
  ushort *puVar1;
  
  puVar1 = (ushort *)(int)DAT_000157da;
  *puVar1 = *puVar1 & (ushort)PTR_DAT_000157f4;
  puVar1[-4] = puVar1[-4] | 0xf;
  puVar1[-2] = puVar1[-2] | 0x55;
  return;
}

