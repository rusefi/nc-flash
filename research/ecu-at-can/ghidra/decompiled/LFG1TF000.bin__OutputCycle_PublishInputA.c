/* Ghidra analysis output; verify against original SH instructions. */

/* Copies8800 toA4DC; stateA4DE priority1 if8804==2 andbothA975/A976bit0,else4 ifanybit2,else3
   ifanybit1,else2. Copiesvalueinallcases. See tcu-cycle-callback.txt. */

uint OutputCycle_PublishInputA(void)

{
  char cVar1;
  undefined2 uVar2;
  bool bVar3;
  undefined *puVar4;
  uint uVar5;
  undefined1 uVar6;
  byte local_c [4];
  byte local_8 [8];
  
  uVar2 = *(undefined2 *)PTR_DAT_00050c18;
  cVar1 = *PTR_DAT_00050c1c;
  (*(code *)PTR_FUN_00050c24)(local_8,PTR_DAT_00050c20,1);
  (*(code *)PTR_FUN_00050c24)(local_c,PTR_DAT_00050c28,1);
  puVar4 = PTR_DAT_00050c14;
  uVar6 = 2;
  if (((cVar1 == '\x02') && ((local_8[0] & 1) == 1)) && ((local_c[0] & 1) == 1)) {
    uVar6 = 1;
    uVar5 = 1;
  }
  else {
    bVar3 = (local_8[0] & 4) == 0;
    if ((bVar3) && ((local_c[0] & 4) == 0)) {
      if (((bVar3) && (uVar5 = 1, (local_8[0] & 2) != 0)) ||
         ((uVar5 = (uint)(char)local_c[0], (uVar5 & 4) == 0 &&
          (uVar5 = -(((local_c[0] & 2) == 0) - 1), uVar5 == 1)))) {
        uVar6 = 3;
      }
    }
    else {
      uVar5 = 1;
      uVar6 = 4;
    }
  }
  *(undefined2 *)PTR_DAT_00050c10 = uVar2;
  *puVar4 = uVar6;
  return uVar5;
}

