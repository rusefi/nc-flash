/* Ghidra analysis output; verify against original SH instructions. */

/* s16(98B2)<102 ->98AE0; gated102..13132 ->1;9924bit0 and>=13133 ->2; otherwisehold.400 independent
   boundary/gate/oldwordcases andcomplete39C90 sideeffects checked. */

void ClassApplication_RetainBandState(void)

{
  undefined2 uVar1;
  
  uVar1 = *(undefined2 *)(int)DAT_00039c12;
  if (((*PTR_DAT_00039c18 & 1) == 1) && (*(short *)PTR_DAT_00039c1c <= *(short *)(int)DAT_00039c14))
  {
    uVar1 = 2;
  }
  if (((((*PTR_DAT_00039c18 & 1) == 1) || ((*PTR_DAT_00039c20 & 0x10) != 0)) ||
      ((*PTR_DAT_00039c24 & 1) == 1)) &&
     ((*(short *)PTR_DAT_00039c28 <= *(short *)(int)DAT_00039c14 &&
      (*(short *)(int)DAT_00039c14 < *(short *)PTR_DAT_00039c1c)))) {
    uVar1 = 1;
  }
  if (*(short *)(int)DAT_00039c14 < *(short *)PTR_DAT_00039c28) {
    uVar1 = 0;
  }
  *(undefined2 *)(int)DAT_00039c12 = uVar1;
  return;
}

