/* Ghidra analysis output; verify against original SH instructions. */

/* Unsigned40E4>=63487 returns1; <2047 returns2; else0. Executed all1024 ADC-aligned samples and
   boundaries. See control-raw-provenance.txt. */

undefined4 Control_ClassifyRawChannel29(void)

{
  undefined4 uVar1;
  
  if (*(ushort *)PTR_DAT_000066e8 < *puRam00006708) {
    if (*(ushort *)PTR_DAT_000066e8 < *puRam0000670c) {
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

