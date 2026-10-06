/* Ghidra analysis output; verify against original SH instructions. */

/* SetsA13C=FF before rotating eight-byte message buffers. See tcu-request-dispatch.txt. */

void EventMessage_InitializeBufferIndex(void)

{
  *(char *)(int)DAT_0004c128 = (char)DAT_0004c126;
  return;
}

