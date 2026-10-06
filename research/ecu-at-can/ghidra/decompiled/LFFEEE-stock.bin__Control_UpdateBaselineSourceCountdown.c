/* Ghidra analysis output; verify against original SH instructions. */

/* 7010 exact1 reloads80A8 from stock DA03C=0; otherwise decrement nonzero byte. All256 counts and
   rawflag0/1/2/255 tested. */

char Control_UpdateBaselineSourceCountdown(void)

{
  undefined *puVar1;
  char cVar2;
  
  puVar1 = PTR_Control_BaselineSourceCountdown_00058c6c;
  cVar2 = (*(code *)PTR_FUN_00058c74)(PTR_DAT_00058c70);
  if (cVar2 == '\x01') {
    *puVar1 = *PTR_DAT_00058c78;
  }
  else if (*puVar1 != '\0') {
    *puVar1 = *puVar1 + (char)DAT_00058c4c;
  }
  return cVar2;
}

