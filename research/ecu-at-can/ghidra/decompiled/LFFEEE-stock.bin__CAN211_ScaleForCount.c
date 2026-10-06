/* Ghidra analysis output; verify against original SH instructions. */

/* For count0..7,7170=715C*8/(8-count); count8 selects0. Nine count cases0..8 verified; Counts
   above8 and count origin/physical meaning open. */

void CAN211_ScaleForCount(void)

{
  float fVar1;
  float fVar2;
  undefined4 uVar3;
  undefined4 uVar4;
  
  uVar4 = 0;
  if (*PTR_Model_PatternCount_0003fbf0 == '\b') {
    *(undefined4 *)PTR_DAT_0003fbf8 = 0;
  }
  else {
    uVar3 = 0x3f800000;
    fVar1 = (float)(*(code *)PTR_FUN_0003fbf4)
                             (0x3f800000,0,8 - (char)*PTR_Model_PatternCount_0003fbf0);
    fVar2 = (float)(*(code *)PTR_FUN_0003fbf4)(uVar3,uVar4,8);
    *(float *)PTR_DAT_0003fbf8 = *(float *)PTR_DAT_0003fbd0 / (fVar1 / fVar2);
  }
  return;
}

