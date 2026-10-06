/* Ghidra analysis output; verify against original SH instructions. */

/* Array6E34: pair1/4 from6E2D and6E29; pair2/3 from6E2C and6E28;6E2A overrides all. */

undefined1 BuildCylinderCutFlags(void)

{
  int iVar1;
  undefined1 uVar2;
  undefined1 *puVar3;
  
  iVar1 = DAT_0003acec;
  puVar3 = (undefined1 *)(DAT_0003acec + 1);
  if (*PTR_DAT_0003acf0 == '\0') {
    if ((*PTR_DAT_0003acf4 == '\x01') && (*PTR_ATCutCountdownPair14_0003acf8 != '\0')) {
      *puVar3 = 1;
      uVar2 = 1;
    }
    else {
      *puVar3 = 0;
      uVar2 = 0;
    }
    *(undefined1 *)(iVar1 + 4) = uVar2;
    if ((*PTR_DAT_0003acfc == '\x01') && (*PTR_ATCutCountdownPair23_0003ad00 != '\0')) {
      *(undefined1 *)(iVar1 + 2) = 1;
      uVar2 = 1;
    }
    else {
      uVar2 = 0;
      *(undefined1 *)(iVar1 + 2) = 0;
    }
    *(undefined1 *)(iVar1 + 3) = uVar2;
  }
  else {
    uVar2 = 1;
    *puVar3 = 1;
    *(undefined1 *)(iVar1 + 2) = 1;
    *(undefined1 *)(iVar1 + 3) = 1;
    *(undefined1 *)(iVar1 + 4) = 1;
  }
  return uVar2;
}

