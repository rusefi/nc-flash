/* Ghidra analysis output; verify against original SH instructions. */

/* Copies87F8 toA518; stateA51A priority1 if87FC==2 andA958bit0,else4 ifbit2,else3 ifbit1,else2.
   Actualsourcefeedsoutputclamp/scaling. See tcu-cycle-callback.txt. */

int OutputCycle_PublishInputB(void)

{
  char cVar1;
  undefined2 uVar2;
  undefined1 uVar3;
  int iVar4;
  byte local_8 [8];
  
  uVar2 = *(undefined2 *)PTR_DAT_0005124c;
  cVar1 = *PTR_DAT_00051250;
  (*(code *)PTR_FUN_00051258)(local_8,PTR_DAT_00051254,1);
  uVar3 = 2;
  if ((cVar1 == '\x02') && ((local_8[0] & 1) == 1)) {
    uVar3 = 1;
    iVar4 = 1;
  }
  else {
    iVar4 = -(((local_8[0] & 4) == 0) - 1);
    if (iVar4 == 1) {
      uVar3 = 4;
    }
    else if ((iVar4 == 0) && (iVar4 = -(((local_8[0] & 2) == 0) - 1), iVar4 == 1)) {
      uVar3 = 3;
    }
  }
  *(undefined2 *)PTR_DAT_00051244 = uVar2;
  *PTR_DAT_00051248 = uVar3;
  return iVar4;
}

