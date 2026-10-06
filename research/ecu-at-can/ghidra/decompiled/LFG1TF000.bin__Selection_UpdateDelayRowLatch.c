/* Ghidra analysis output; verify against original SH instructions. */

/* Updates9C79bit1 fromsigned9340 thresholds7735C=-5120/7735E=256 and92D5bit0/oldbit2.
   Usedinexecuted37/18-count candidatefixtures; sourceunitsunproved. */

void Selection_UpdateDelayRowLatch(void)

{
  byte bVar1;
  char cVar2;
  int iVar3;
  
  iVar3 = (int)DAT_00048acc;
  cVar2 = -(((*(byte *)(iVar3 + 1) & 2) == 0) + -1);
  if ((((*(byte *)(iVar3 + 1) & 4) == 0) && ((*PTR_ApplicationFaultFlags92D5_00048adc & 1) == 1)) ||
     (*(short *)PTR_DAT_00048ad8 < *(short *)PTR_DAT_00048ae0)) {
    cVar2 = '\x01';
  }
  if (((*PTR_ApplicationFaultFlags92D5_00048adc & 1) == 0) &&
     (*(short *)PTR_DAT_00048ae4 <= *(short *)PTR_DAT_00048ad8)) {
    cVar2 = '\0';
  }
  if (cVar2 == '\0') {
    bVar1 = *(byte *)(iVar3 + 1) & 0xfd;
  }
  else {
    bVar1 = *(byte *)(iVar3 + 1) | 2;
  }
  *(byte *)(iVar3 + 1) = bVar1;
  return;
}

