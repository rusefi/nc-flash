/* Ghidra analysis output; verify against original SH instructions. */

/* Returns ROM76E46<<12; stock14*4096=57344; input cap and reset history value. See
   tcu-reference-source.txt. */

int Reference_ReadResetPeriod(void)

{
  return (uint)(byte)*PTR_DAT_00020e40 << 0xc;
}

