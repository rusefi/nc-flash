/* Ghidra analysis output; verify against original SH instructions. */

/* Returns word736A. Complete1FB5A caller ->20290 ->timer-register writes verified
   inoutput-inhibition.txt. Pin routing remains unproved. */

int Pattern_GetCylinderInhibitMask(void)

{
  return (int)*(short *)PTR_DAT_0001f984;
}

