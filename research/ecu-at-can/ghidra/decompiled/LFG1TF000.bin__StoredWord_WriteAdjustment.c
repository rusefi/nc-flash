/* Ghidra analysis output; verify against original SH instructions. */

/* Write low16R5 at616A+2*u16R4,return0.49FE0 producer usesindices6/7/8;13,098wholeproducercases
   and18retained traces pass. */

undefined4 StoredWord_WriteAdjustment(uint param_1,undefined2 param_2)

{
  *(undefined2 *)((param_1 & 0xffff) * 2 + DAT_000245d0) = param_2;
  return 0;
}

