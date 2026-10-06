/* Ghidra analysis output; verify against original SH instructions. */

/* Four cylinder status bits ->736A mask via8B5C0; nonzero ->7368. Diagnostic overlay may add bits.
    */

uint AggregateCylinderCutMask(void)

{
  undefined *puVar1;
  uint uVar2;
  uint uVar3;
  
  uVar3 = 0;
  uVar2 = DAT_00042f9c;
  if ((*PTR_DAT_00042f94 != '\x01') && (*PTR_DAT_00042f98 != '\0')) {
    if (((PTR_DAT_00042fa0[1] & 0x40) != 0) || (((int)(char)*PTR_DAT_00042fa4 & 0x80U) != 0)) {
      uVar3 = 1;
    }
    if (((PTR_DAT_00042fa0[2] & 0x40) != 0) || (((int)(char)*PTR_DAT_00042fa8 & 0x80U) != 0)) {
      uVar3 = uVar3 | 2;
    }
    if (((PTR_DAT_00042fa0[3] & 0x40) != 0) || (((int)(char)*PTR_DAT_00042fac & 0x80U) != 0)) {
      uVar3 = uVar3 | 4;
    }
    if (((PTR_DAT_00042fa0[4] & 0x40) != 0) ||
       (uVar2 = uVar3, ((int)(char)*PTR_DAT_00042fb0 & 0x80U) != 0)) {
      uVar2 = uVar3 | 8;
    }
  }
  uVar2 = (*(code *)PTR_FUN_00042fb4)(uVar2);
  puVar1 = PTR_DAT_00042fbc;
  *(short *)PTR_DAT_00042fb8 = (short)uVar2;
  if ((uVar2 & 0xffff) == 0) {
    uVar2 = 0;
    *puVar1 = 0;
  }
  else {
    *puVar1 = 1;
  }
  return uVar2;
}

