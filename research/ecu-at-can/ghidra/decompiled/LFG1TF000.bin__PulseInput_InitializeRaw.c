/* Ghidra analysis output; verify against original SH instructions. */

/* Executed: clears88CC/88CD; see tcu-pulse-input.txt. */

void PulseInput_InitializeRaw(void)

{
  undefined *puVar1;
  
  puVar1 = PTR_PulseInput_RawStatus_00017698;
  *PTR_PulseInput_RawBit_00017694 = 0;
  *puVar1 = 0;
  return;
}

