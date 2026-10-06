/* Ghidra analysis output; verify against original SH instructions. */

/* Executed reverse code lookup0704->43 and0850->44; general unknown-code behavior not tested. */

uint Diagnostic_FindCodeIndex(short param_1)

{
  uint uVar1;
  
  for (uVar1 = 0;
      (*(short *)(DAT_0009036c + (uVar1 & 0xffff) * 2) != param_1 &&
      ((int)(uVar1 & 0xffff) < (int)DAT_00090366)); uVar1 = uVar1 + 1) {
  }
  return uVar1;
}

