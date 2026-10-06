/* Ghidra analysis output; verify against original SH instructions. */

/* ReturnsA666 unlessA668==1, thenA667. SelectedA665 reaches CAN231 byte1 bit6 through19414/1C39A.
    */

int Diagnostic_GetActiveOutputOverride(void)

{
  char cVar1;
  
  cVar1 = *(char *)(int)DAT_000532ee;
  if (*(char *)(int)DAT_000532f2 == '\x01') {
    cVar1 = *(char *)(int)DAT_000532f0;
  }
  return (int)cVar1;
}

