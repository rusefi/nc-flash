/* Ghidra analysis output; verify against original SH instructions. */

/* 8197=(RTZ(8028-801C)>=DAC58=20266). Executedby58338evenratioheldorcleared. */

void Control_UpdateSourceDeltaHigh(void)

{
  if (*(float *)PTR_Control_RetainedSourceRatio_0005ab74 - *DAT_0005ab70 <
      *(float *)PTR_DAT_0005ab7c) {
    *PTR_DAT_0005ab78 = 0;
  }
  else {
    *PTR_DAT_0005ab78 = 1;
  }
  return;
}

