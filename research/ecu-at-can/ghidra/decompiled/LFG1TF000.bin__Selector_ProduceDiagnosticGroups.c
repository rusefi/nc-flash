/* Ghidra analysis output; verify against original SH instructions. */

/* Input count and A938/A735 gates produce groups15/16 codes0707/0708. Missing-input path
   uses843E=2000 then8440=28000 with80BA>=300 and A962 bit0. Input3 alone plus88BA/88BC zero
   publishes recovery bit80; see selector-recovery.txt. */

void Selector_ProduceDiagnosticGroups(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  byte bVar4;
  char cVar5;
  char cVar6;
  undefined4 uVar7;
  undefined2 uVar8;
  int iVar9;
  uint uVar10;
  
  puVar3 = PTR_DAT_00058600;
  puVar2 = PTR_DAT_000585fc;
  puVar1 = PTR_DAT_000585f8;
  uVar10 = 0;
  iVar9 = 0;
  uVar7 = 0;
  uVar8 = SUB42(PTR_DAT_000585f8,0);
  if ((*PTR_DAT_00058604 == '\x01') && (*PTR_DAT_00058608 == '\0')) {
    iVar9 = 1;
    uVar7 = 1;
    uVar10 = (uint)((*PTR_SpeedFault_Group13Summary_0005860c & 1) == 1);
    bVar4 = Selector_CountAssertedInputs();
    if (bVar4 == 0) {
      if (uVar10 == 1) {
        if ((undefined *)(uint)*(ushort *)puVar2 == puVar1) {
          *(undefined2 *)puVar2 = DAT_000585f0;
        }
        if (((int)(uint)DAT_ffff80ba < (int)DAT_000585f2) || (*(short *)PTR_DAT_000585fc != 0)) {
          *(undefined2 *)puVar3 = uVar8;
        }
        else if ((undefined *)(uint)*(ushort *)puVar3 == puVar1) {
          *(undefined2 *)puVar3 = DAT_000585f4;
        }
        if (*(short *)puVar2 == 0) {
          uVar10 = 3;
        }
        if (*(short *)puVar3 == 0) {
          uVar10 = uVar10 | 6;
        }
        goto LAB_00058644;
      }
    }
    else if (bVar4 < 2) {
      cVar5 = Selector_CheckInputThreeOnly();
      if (cVar5 == '\x01') {
        uVar7 = 3;
        cVar5 = (*(code *)PTR_FUN_000586c8)(0x16);
        cVar6 = (*(code *)PTR_FUN_000586c8)(0x15);
        if (cVar5 != '\0') {
          uVar10 = uVar10 | (int)DAT_000586c2;
        }
        if (cVar6 != '\0') {
          iVar9 = (int)DAT_000586c4;
        }
      }
    }
    else {
      iVar9 = 3;
    }
  }
  *(undefined2 *)puVar2 = uVar8;
  *(undefined2 *)puVar3 = uVar8;
LAB_00058644:
  (*(code *)PTR_Diagnostic_StoreGroupStatus_000586cc)(0x16,uVar10);
  (*(code *)PTR_Diagnostic_StoreGroupStatus_000586cc)(0x15,iVar9);
  (*(code *)PTR_Diagnostic_StoreMappedStatus_000586d0)(0xc,uVar7);
  return;
}

