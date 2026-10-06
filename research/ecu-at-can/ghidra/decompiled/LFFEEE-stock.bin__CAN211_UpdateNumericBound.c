/* Ghidra analysis output; verify against original SH instructions. */

/* Stock C11E9=0;718E ramp path,7190/7191 inhibition, otherwise u16[6A1C]-10000 ->protected714C.
   Physical units and full arbitration unresolved. */

void CAN211_UpdateNumericBound(void)

{
  char cVar1;
  float fVar2;
  undefined4 uVar3;
  
  fVar2 = (float)(*(code *)PTR_FUN_000400ac)(PTR_CAN211_NumericBound_000400a8);
  if (*PTR_DAT_000400b0 == '\0') {
    uVar3 = DAT_000400b8;
    if (*PTR_DAT_000400bc == '\x01') {
      cVar1 = (*(code *)PTR_FUN_000400c4)(PTR_DAT_000400c0);
      if ((cVar1 != '\x01') && (fVar2 <= *(float *)PTR_DAT_000400c8)) {
        uVar3 = (*(code *)PTR_FUN_000400d0)(*(float *)PTR_DAT_000400cc + fVar2,uVar3);
      }
    }
    else if ((*PTR_DAT_000400d4 != '\x01') && (*PTR_DAT_000400d8 != '\x01')) {
      uVar3 = (*(code *)PTR_FUN_000400e4)
                        (0x3f800000,DAT_000400dc,(int)*(short *)PTR_CAN211_FreshWord0_000400e0);
    }
  }
  else {
    uVar3 = *(undefined4 *)PTR_DAT_000400b4;
  }
  (*(code *)PTR_FUN_000400e8)(uVar3,PTR_CAN211_NumericBound_000400a8);
  return;
}

