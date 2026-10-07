/* Ghidra analysis output; verify against original SH instructions. */

/* Executed3072wholeRAM cases:4040>>6 to6C92,4042>>8 to6CAE,4046 to6C98. RTS
   delaywrite;SR/GPR8..15/GBR preserved. Sixactual1B132 returns1B136
   checkedin120queued-acquisition/event2 pairs:ADC28recovery copied64,published/qualified65,mode2
   reports1F/20. Explicitinterleave/serialsamples, notphysicalcadence.
   control-acquired-qualification.txt. */

void Acquisition_DecodeSlowBankInputs(void)

{
  undefined *puVar1;
  
  puVar1 = PTR_Acquisition_ADCResultBank_00039960;
  *(ushort *)PTR_DAT_00039968 = *(ushort *)(PTR_Acquisition_ADCResultBank_00039960 + 0x38) >> 6;
  *PTR_DAT_0003996c = (char)((ushort)*(undefined2 *)(puVar1 + 0x3a) >> 8);
  *(undefined2 *)PTR_DAT_00039984 = *(undefined2 *)(puVar1 + 0x3e);
  return;
}

