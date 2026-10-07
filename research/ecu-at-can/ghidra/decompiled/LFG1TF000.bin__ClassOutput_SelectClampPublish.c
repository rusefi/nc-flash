/* Ghidra analysis output; verify against original SH instructions. */

/* Stock5CCE4={1,0} disables910A;9C58bit0forces0; lastnonsentinel9108 clamps0..15232 ->8100;
   times100>>8 ->80AC and53070index1. AllRAMindependentlyverified; tcu-base-publication.txt. */

void ClassOutput_SelectClampPublish(void)

{
  short sVar1;
  short sVar2;
  undefined *puVar3;
  short sVar5;
  undefined4 uVar4;
  int iVar6;
  int iVar7;
  int iVar8;
  undefined2 local_28 [6];
  
  puVar3 = PTR_DAT_0001f398;
  sVar1 = *(short *)PTR_PTR_0001f384;
  sVar2 = *(short *)PTR_DAT_0001f394;
  iVar6 = (int)DAT_0001f380;
  iVar7 = 0;
  do {
    if (puVar3[iVar7] == '\0') {
      FUN_0001f29e(iVar7);
    }
    iVar8 = iVar7 + 1;
    local_28[iVar7] = *(undefined2 *)(iVar6 + iVar7 * 2);
    iVar7 = iVar8;
  } while (iVar8 < 2);
  sVar5 = sVar1;
  if ((*PTR_Selection_InhibitFlags_0001f39c & 1) != 1) {
    sVar5 = (*(code *)PTR_Request_SelectLastWord_0001f3a0)(iVar6,2,(int)sVar1);
  }
  ClassOutput_ClampedWord = sVar1;
  if ((sVar1 < sVar5) && (ClassOutput_ClampedWord = sVar5, sVar2 <= sVar5)) {
    ClassOutput_ClampedWord = sVar2;
  }
  uVar4 = (*(code *)PTR_FUN_0001f388)();
  (*(code *)PTR_OutputRecord_PublishWord_0001f3a4)(1,uVar4);
  ClassOutput_ScaledWord = (short)uVar4;
  return;
}

