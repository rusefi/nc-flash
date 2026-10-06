/* Ghidra analysis output; verify against original SH instructions. */

/* Low-byte argument exactly1 AND class8080==6 AND916Dbit3 clear.7168 cases. Caller495C0
   supplies9316bit0; physical mode unresolved. */

undefined4 SourcePolicy_CheckAdmission(char param_1)

{
  undefined4 uVar1;
  
  uVar1 = 0;
  if (((param_1 == '\x01') && (TransmissionStateClass == 6)) && ((*PTR_DAT_0004994c & 8) == 0)) {
    uVar1 = 1;
  }
  return uVar1;
}

