/* Ghidra analysis output; verify against original SH instructions. */

/* Ten eight-byte buffers atA140; increment index andwrap10. Executed request and release messages;
   general concurrent ownership open. See tcu-request-dispatch.txt. */

int EventMessage_NextBuffer(void)

{
  byte *pbVar1;
  
  pbVar1 = (byte *)(int)DAT_0004c128;
  *pbVar1 = *pbVar1 + 1;
  if (9 < *pbVar1) {
    *pbVar1 = 0;
  }
  return (int)DAT_0004c12a + (uint)*pbVar1 * 8;
}

