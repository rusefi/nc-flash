/* Ghidra analysis output; verify against original SH instructions. */

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* 1024originalcases:write3C-keyed lowbyteR4 toSYSCR2 F70A thenfourNOPs.
   Localmodelpreservesone-wayFPUstop;physicalclock/reset/UBC/AUDnotmodeled.
   control-initialize-syscr.txt. */

void Hardware_WriteSystemControl2(ushort param_1)

{
  _DAT_fffff70a = param_1 & 0xff | 0x3c00;
  return;
}

