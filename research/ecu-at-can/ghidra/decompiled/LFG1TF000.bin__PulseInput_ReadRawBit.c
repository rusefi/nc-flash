/* Ghidra analysis output; verify against original SH instructions. */

/* Executed:88CC=(8F33>>1)&1;88CD=2. Physical input and actual scheduler cadence unproved. */

void PulseInput_ReadRawBit(void)

{
  undefined *puVar1;
  
  puVar1 = PTR_PulseInput_RawStatus_00017698;
  *PTR_PulseInput_RawBit_00017694 = (*PTR_PulseInput_RawBitfield_0001769c & 2) != 0;
  *puVar1 = 2;
  return;
}

