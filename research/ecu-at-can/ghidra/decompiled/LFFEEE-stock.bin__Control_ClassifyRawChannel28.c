/* Ghidra analysis output; verify against original SH instructions. */

/* Unsigned40F8>=58327 returns1; <2559 returns2; else0. Executed ADC-aligned samples/boundaries. See
   control-raw-provenance.txt. */

undefined4 Control_ClassifyRawChannel28(void)

{
  undefined4 uVar1;
  
  if (*(ushort *)PTR_DAT_00007094 < *(ushort *)PTR_DAT_000070b4) {
    if (*(ushort *)PTR_DAT_00007094 < *(ushort *)PTR_DAT_000070b8) {
      uVar1 = 2;
    }
    else {
      uVar1 = 0;
    }
  }
  else {
    uVar1 = 1;
  }
  return uVar1;
}

