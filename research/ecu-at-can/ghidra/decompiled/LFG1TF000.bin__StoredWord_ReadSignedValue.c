/* Ghidra analysis output; verify against original SH instructions. */

/* Signedword616A+2*u16R4, readRTSdelayslot.140pairedaccessorcases including indextruncation;
   tcu-stored-adjustments.txt. */

int StoredWord_ReadSignedValue(ushort param_1)

{
  return (int)*(short *)(DAT_000245d0 + (uint)param_1 * 2);
}

