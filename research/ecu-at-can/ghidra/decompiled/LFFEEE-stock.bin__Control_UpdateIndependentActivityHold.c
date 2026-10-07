/* Ghidra analysis output; verify against original SH instructions. */

/* Executed28672cases:mode735Abit7 increments9158saturating,elseholds.915E1 clearsprotected2444
   and915E,NOT9158;elseactivecount>=1 writes2444=1.915C iffactiveupdatedcount<3.
   Eightactualtaskreturns;usesprior735A beforecurrentmodeupdate. */

char Control_UpdateIndependentActivityHold(void)

{
  ushort uVar1;
  undefined2 uVar2;
  char cVar3;
  
  uVar1 = (*(code *)PTR_FUN_00075090)
                    ((int)*(short *)PTR_DAT_0007508c,(int)*(short *)PTR_DAT_00075088);
  cVar3 = -((((int)(char)*PTR_DAT_00075094 & 0x80U) == 0) + -1);
  if (cVar3 == '\x01') {
    uVar2 = (*(code *)PTR_FUN_00075090)((int)*(short *)PTR_DAT_00075098,1);
    *(undefined2 *)PTR_DAT_00075098 = uVar2;
  }
  if (*PTR_DAT_0007509c == '\x01') {
    (*(code *)PTR_FUN_00075084)(PTR_DAT_00075078,0);
    *PTR_DAT_0007509c = 0;
  }
  else if ((cVar3 == '\x01') && (*(ushort *)PTR_DAT_0007508c <= *(ushort *)PTR_DAT_00075098)) {
    (*(code *)PTR_FUN_00075084)(PTR_DAT_00075078,1);
  }
  if ((cVar3 == '\x01') && (*(ushort *)PTR_DAT_00075098 < uVar1)) {
    *PTR_Control_IndependentActivityHold_000750a0 = 1;
  }
  else {
    *PTR_Control_IndependentActivityHold_000750a0 = 0;
  }
  return cVar3;
}

