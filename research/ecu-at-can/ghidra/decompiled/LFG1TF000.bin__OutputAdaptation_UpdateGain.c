/* Ghidra analysis output; verify against original SH instructions. */

/* Strict base/error/normalized-error gates. Compute target3700..9700, step arithmetic>>4
   clamped+-100. First8ABDzero update uses fullstep and optional4788+223*89A8/10. Nonzero89AC
   enables gainupdate with integral compensation; derivedgains rescale evenwhendisabled.3368
   cases/19 retainedadmissions; see tcu-output-adaptation.txt. */

int OutputAdaptation_UpdateGain(uint param_1)

{
  undefined *puVar1;
  short sVar2;
  undefined2 uVar3;
  int *piVar4;
  undefined4 uVar5;
  char *pcVar6;
  int iVar7;
  int iVar8;
  int iVar9;
  
  puVar1 = PTR_OutputDriver_CurrentWords_00018d8c;
  iVar7 = (int)DAT_00018d70;
  iVar9 = (param_1 & 0xff) * 2;
  uVar5 = 0;
  if (*(short *)(PTR_OutputDriver_CurrentWords_00018d8c + iVar9) != 0) {
    uVar5 = (*(code *)PTR_FUN_00018d90)();
  }
  if ((((((int)DAT_00018d74 <= (int)(uint)*(ushort *)(puVar1 + iVar9)) &&
        (*(short *)(iVar7 + iVar9) < *(short *)(int)DAT_00018d76)) &&
       (*(short *)(int)DAT_00018d78 < *(short *)(iVar7 + iVar9))) &&
      (((short)uVar5 < *(short *)(int)DAT_00018d7a && (*(short *)(int)DAT_00018d7c < (short)uVar5)))
      ) && (*(short *)(puVar1 + iVar9) != 0)) {
    (*(code *)PTR_FUN_00018d90)(uVar5,(int)DAT_00018d80,(int)DAT_00018d7e);
    uVar5 = (*(code *)PTR_FUN_00018d90)();
    iVar7 = (*(code *)PTR_FUN_00018d94)(uVar5);
    iVar8 = (int)DAT_00018d84;
    sVar2 = (*(code *)PTR_FUN_00018d94)
                      ((int)(short)iVar7 - (int)*(short *)(iVar9 + iVar8) >> 4,0xffffff9c,100);
    uVar3 = (*(code *)PTR_FUN_00018d98)(iVar7 - *(short *)(iVar9 + iVar8));
    *(undefined2 *)(DAT_00018d86 + iVar9) = uVar3;
    pcVar6 = (char *)((param_1 & 0xff) + (int)DAT_00018d88);
    if ((*pcVar6 == '\0') && (*(short *)(iVar9 + DAT_00018d86) < *(short *)PTR_DAT_00018d9c)) {
      *pcVar6 = '\x01';
    }
    if (*PTR_DAT_00018da0 != '\0') {
      if (*(char *)((param_1 & 0xff) + (int)DAT_00018d8a) == '\0') {
        if ((*(ushort *)PTR_DAT_00018da8 <= *(ushort *)PTR_DAT_00018da4) &&
           (*(ushort *)PTR_DAT_00018da4 <= *(ushort *)PTR_DAT_00018eec)) {
          iVar7 = (*(code *)PTR_FUN_00018ef4)
                            ((int)*(short *)PTR_CutLookup_SourceValue_00018ef0,(int)DAT_00018eca,10)
          ;
          iVar7 = DAT_00018ecc + iVar7;
        }
        sVar2 = (short)iVar7 - *(short *)(iVar8 + iVar9);
        *(undefined1 *)((param_1 & 0xff) + (int)DAT_00018ece) = 1;
      }
      piVar4 = (int *)((int)DAT_00018ed0 + (param_1 & 0xff) * 4);
      *piVar4 = *piVar4 - (uint)*(ushort *)(PTR_OutputDriver_CurrentWords_00018ef8 + iVar9) *
                          (int)sVar2;
      *(short *)(iVar9 + iVar8) = sVar2 + *(short *)(iVar9 + iVar8);
    }
    uVar3 = (*DAT_00018efc)();
    *(undefined2 *)(DAT_00018ed6 + iVar9) = uVar3;
    iVar7 = (*DAT_00018efc)();
    *(short *)(DAT_00018eda + iVar9) = (short)iVar7;
    iVar9 = iVar7;
  }
  return iVar9;
}

