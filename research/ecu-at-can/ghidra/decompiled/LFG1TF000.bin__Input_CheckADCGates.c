/* Ghidra analysis output; verify against original SH instructions. */

/* Mask1 checks ADC FFFFF810 count>=375; mask2 checks FFFFF812 count>=373. Returns1 on any selected
   failure. Executed with fixed register samples. */

undefined4 Input_CheckADCGates(byte param_1)

{
  ushort uVar1;
  undefined4 uVar2;
  
  uVar2 = 0;
  uVar1 = (*(code *)PTR_OutputHandoff_ReadAdcCount_000143cc)(PTR_DAT_000143c8);
  if (((param_1 & 1) == 1) && (uVar1 < *(ushort *)PTR_DAT_000143d0)) {
    uVar2 = 1;
  }
  uVar1 = (*(code *)PTR_OutputHandoff_ReadAdcCount_000143cc)(PTR_DAT_000143d4);
  if (((param_1 & 2) == 2) && (uVar1 < *(ushort *)PTR_DAT_000143d8)) {
    uVar2 = 1;
  }
  return uVar2;
}

