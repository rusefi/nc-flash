/* Ghidra analysis output; verify against original SH instructions. */

/* min(2*u16(input),FFFF); original helper executes in captured-axis and full upstream tests. */

undefined * Request_DoubleCapturedAxis(uint param_1)

{
  undefined *puVar1;
  
  puVar1 = (undefined *)((param_1 & 0xffff) << 1);
  if (PTR_DAT_0003151c < puVar1) {
    puVar1 = PTR_DAT_0003151c;
  }
  return puVar1;
}

