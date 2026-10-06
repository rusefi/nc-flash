/* Ghidra analysis output; verify against original SH instructions. */

/* 8198=(RTZ(8028-801C)<=0). Executedby58338evenratioheldorcleared. */

void Control_UpdateSourceDeltaNonpositive(void)

{
  if (0.0 < *(float *)PTR_Control_RetainedSourceRatio_0005ab74 - *DAT_0005ab70) {
    *PTR_DAT_0005ab80 = 0;
  }
  else {
    *PTR_DAT_0005ab80 = 1;
  }
  return;
}

