/* Ghidra analysis output; verify against original SH instructions. */

/* Executed108 cases:735A=80 if735Czero or6604exact1;else40 if6536zero or73C4bit7;else20. FullRAM
   oracle. control-activity-hooks.txt. */

char Control_SelectHeldModeBits(void)

{
  char cVar1;
  char cVar2;
  
  if ((*PTR_Control_ModeHoldFlag_00042b58 == '\0') || (*PTR_DAT_00042b7c == '\x01')) {
    cVar1 = '\0';
  }
  else if ((*PTR_DAT_00042c48 == '\0') || (((int)(char)*PTR_DAT_00042c4c & 0x80U) != 0)) {
    cVar1 = '\x01';
  }
  else {
    cVar1 = '\x02';
  }
  if (cVar1 == '\0') {
    cVar2 = (char)DAT_00042c44;
  }
  else if (cVar1 == '\x01') {
    cVar2 = '@';
  }
  else {
    cVar2 = cVar1;
    if (cVar1 == '\x02') {
      cVar2 = ' ';
    }
  }
  *PTR_DAT_00042c50 = cVar2;
  return cVar1;
}

