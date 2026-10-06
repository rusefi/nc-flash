/* Ghidra analysis output; verify against original SH instructions. */

/* Exhausted all65536 runtime masks for43/44: stock AC008 word entries0000 always return1 and reject
   dispatch. */

bool Diagnostic_CheckRuntimeMaskAbsent(uint param_1,ushort param_2)

{
  return (param_2 & *(ushort *)(PTR_DAT_00090378 + (param_1 & 0xffff) * 2)) == 0;
}

