/* Ghidra analysis output; verify against original SH instructions. */

/* Exhausted all65536 runtime masks pergroup:43/44 stock entries0000 alwaysreject;1F/20 entries8000
   returnzero exactlywhen runtimebit8000 admits. No downstream lifecycle inference. */

bool Diagnostic_CheckRuntimeMaskAbsent(uint param_1,ushort param_2)

{
  return (param_2 & *(ushort *)(PTR_DAT_00090378 + (param_1 & 0xffff) * 2)) == 0;
}

