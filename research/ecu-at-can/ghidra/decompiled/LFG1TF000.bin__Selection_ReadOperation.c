/* Ghidra analysis output; verify against original SH instructions. */

/* Returns9C88; used in descending phase counter threshold override, exercised with values0/5. */

int Selection_ReadOperation(void)

{
  return (int)*(char *)(int)DAT_00048e0c;
}

