/* Ghidra analysis output; verify against original SH instructions. */

/* Copies95AEbit0 torecord+18bit20 onstate3entry. Later duration/map selection uses capturedflag.
   See tcu-request-dispatch.txt. */

uint SparkRequest_CaptureSpecialFlag(int param_1)

{
  uint uVar1;
  
  if ((*PTR_DAT_0004d83c & 1) == 0) {
    uVar1 = (int)*(char *)(param_1 + 0x12) & 0xdf;
    *(char *)(param_1 + 0x12) = (char)uVar1;
  }
  else {
    uVar1 = (int)*(char *)(param_1 + 0x12) | 0x20;
    *(char *)(param_1 + 0x12) = (char)uVar1;
  }
  return uVar1;
}

