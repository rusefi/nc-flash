/* Ghidra analysis output; verify against original SH instructions. */

/* Abort exact1 clears985C; otherwise failed36BDA returns state1. Stock equal calibration bounds
   ensure failure. Executes before periodic update counter. */

int ClassAdjustment_State2(void)

{
  char cVar1;
  char cVar2;
  
  cVar1 = ClassAdjustment_ModeAbort();
  cVar2 = ClassAdjustment_StockAdmission();
  if (cVar1 == 1) {
    *(undefined1 *)(int)DAT_00036c96 = 0;
  }
  else if (cVar2 == '\0') {
    *(undefined1 *)(int)DAT_00036c96 = 1;
  }
  return (int)cVar1;
}

