/* Ghidra analysis output; verify against original SH instructions. */

/* Static:89F2/89F5 andA991 diagnostic selection ->A552; full producer not yet executed. */

int SpeedCandidate_SelectScalingInputs(void)

{
  char cVar1;
  char cVar2;
  undefined *puVar3;
  int iVar4;
  undefined1 uVar5;
  undefined1 uVar6;
  undefined2 uVar7;
  undefined2 uVar8;
  byte local_c [4];
  byte local_8 [8];
  
  puVar3 = PTR_DAT_00051c14;
  cVar1 = *PTR_DAT_00051c0c;
  cVar2 = *PTR_DAT_00051c10;
  (*(code *)PTR_FUN_00051c18)(local_8,PTR_DAT_00051c14,1);
  (*(code *)PTR_FUN_00051c18)(local_c,puVar3,1);
  uVar6 = 2;
  uVar7 = *(undefined2 *)PTR_DAT_00051bfc;
  uVar8 = *(undefined2 *)PTR_SpeedCandidate_ScalingInput_00051c00;
  uVar5 = 2;
  if ((cVar1 == '\x02') && ((local_8[0] & 1) == 1)) {
    uVar7 = *(undefined2 *)PTR_DAT_00051c1c;
    uVar5 = 1;
  }
  else if ((local_8[0] & 4) == 0) {
    if ((local_8[0] & 2) != 0) {
      uVar5 = 3;
    }
  }
  else {
    uVar7 = *(undefined2 *)PTR_DAT_00051c20;
    uVar5 = 4;
  }
  if ((cVar2 == '\x02') && ((local_c[0] & 1) == 1)) {
    uVar8 = *(undefined2 *)PTR_DAT_00051c24;
    uVar6 = 1;
    iVar4 = 1;
  }
  else if ((local_c[0] & 4) == 0) {
    iVar4 = -(((local_c[0] & 2) == 0) - 1);
    if (iVar4 == 1) {
      uVar6 = 3;
    }
  }
  else {
    uVar8 = *(undefined2 *)PTR_DAT_00051c20;
    uVar6 = 4;
    iVar4 = 1;
  }
  *(undefined2 *)PTR_DAT_00051bfc = uVar7;
  *(undefined2 *)PTR_SpeedCandidate_ScalingInput_00051c00 = uVar8;
  *PTR_DAT_00051c04 = uVar5;
  *PTR_DAT_00051c08 = uVar6;
  return iVar4;
}

