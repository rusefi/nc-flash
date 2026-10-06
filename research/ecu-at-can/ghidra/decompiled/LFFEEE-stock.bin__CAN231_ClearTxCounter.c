/* Ghidra analysis output; verify against original SH instructions. */

/* Writes6B6C=0. Two25-call lifecycles verify admitted versus inhibited service behavior; physical
   tick duration unknown. */

void CAN231_ClearTxCounter(void)

{
  *(undefined2 *)PTR_CAN231_ECUTxCounter_00036e14 = 0;
  return;
}

