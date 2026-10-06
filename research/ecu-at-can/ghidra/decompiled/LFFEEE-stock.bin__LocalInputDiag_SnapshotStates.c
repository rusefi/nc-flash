/* Ghidra analysis output; verify against original SH instructions. */

/* Executed snapshot after counter update in original1B952 caller segment:
   Boolean7244->8EB7,723E->8EBB. */

bool LocalInputDiag_SnapshotStates(void)

{
  char cVar1;
  
  cVar1 = (*(code *)PTR_FUN_0006c154)(PTR_DAT_0006c150);
  if (cVar1 == '\0') {
    *PTR_DAT_0006c158 = 0;
  }
  else {
    *PTR_DAT_0006c158 = 1;
  }
  cVar1 = (*(code *)PTR_FUN_0006c154)(PTR_DAT_0006c15c);
  if (cVar1 != '\0') {
    *DAT_0006c160 = 1;
  }
  else {
    *DAT_0006c160 = 0;
  }
  return cVar1 != '\0';
}

