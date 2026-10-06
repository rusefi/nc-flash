/* Ghidra analysis output; verify against original SH instructions. */

/* u16 pointer argument: decrement nonzero value except FFFF; seven boundary vectors pass. */

void Timer_DecrementWordUnlessSentinel(ushort *param_1)

{
  if (((undefined *)(uint)*param_1 != PTR_DAT_00011dd4) &&
     ((undefined *)(uint)*param_1 != (undefined *)0x0)) {
    *param_1 = (short)PTR_DAT_00011dd4 + *param_1;
  }
  return;
}

