/* Ghidra analysis output; verify against original SH instructions. */

/* StoreslowbyteR5 using signedbyteR4 index into910D via3064C. Validindices0..10verified;
   genericboundsnotprovided. See tcu-source-inhibit.txt. */

void DiscreteOutput_SetSlot(undefined4 param_1,undefined4 param_2)

{
  (*DAT_0001f480)((int)DAT_0001f476,param_1,param_2);
  return;
}

