/* Ghidra analysis output; verify against original SH instructions. */

/* Sign-extended byte getter used by admission checks2F0C2/2F4F4. Upstream producer and physical
   role unproved. */

int Transition_ReadState9564(void)

{
  return (int)*(char *)(int)DAT_0002dbbe;
}

