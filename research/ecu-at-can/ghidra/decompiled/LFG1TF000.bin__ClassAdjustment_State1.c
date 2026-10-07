/* Ghidra analysis output; verify against original SH instructions. */

/* Calls36CEC/36BDA/36CD8. Abort exact1 clears985C; otherwise admission+timer exact1 enters2.
   Stock36BDA always0, so cannot enter2. Executed through full369A4. */

int ClassAdjustment_State1(void)

{
  char cVar2;
  char cVar3;
  char cVar4;
  int iVar1;
  
  cVar2 = ClassAdjustment_ModeAbort();
  cVar3 = ClassAdjustment_StockAdmission();
  cVar4 = ClassAdjustment_TimerAdmission();
  if (cVar2 == '\x01') {
    *(undefined1 *)(int)DAT_00036b8e = 0;
    iVar1 = 1;
  }
  else {
    iVar1 = (int)cVar3;
    if ((iVar1 == 1) && (iVar1 = (int)cVar4, iVar1 == 1)) {
      *(undefined1 *)(int)DAT_00036b8e = 2;
    }
  }
  return iVar1;
}

