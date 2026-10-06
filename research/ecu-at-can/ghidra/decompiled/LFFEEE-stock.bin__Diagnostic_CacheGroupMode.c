/* Ghidra analysis output; verify against original SH instructions. */

/* Executed writes mode byte at971E+u16(group), returns cached byte. */

int Diagnostic_CacheGroupMode(ushort param_1,char param_2)

{
  char *pcVar1;
  
  pcVar1 = PTR_DAT_0008fd84 + param_1;
  *pcVar1 = param_2;
  return (int)*pcVar1;
}

