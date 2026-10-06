/* Ghidra analysis output; verify against original SH instructions. */

/* Twelve arithmetic right shifts ofR0, including RTS delay slot. Original helper used in2117C;
   signed negative rounding toward minus infinity verified. */

int FixedPoint_ShiftSignedBy12(void)

{
  int in_r0;
  
  return in_r0 >> 0xc;
}

