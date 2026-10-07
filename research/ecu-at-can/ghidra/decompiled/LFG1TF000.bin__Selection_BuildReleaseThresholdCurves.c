/* Ghidra analysis output; verify against original SH instructions. */

/* Alltenheaders; release1 installsupperFFFFonly,lowerdescriptors/valuespreserved.
   Normaltenconstantcurves via460E0,baseline+192,unsignedminimum; op5/kind6. Sourceunchanged. */

uint Selection_BuildReleaseThresholdCurves(char param_1)

{
  byte bVar1;
  short sVar2;
  short sVar3;
  undefined *puVar4;
  undefined *puVar5;
  undefined2 uVar6;
  short sVar7;
  ushort uVar8;
  int iVar9;
  uint uVar10;
  undefined2 *puVar11;
  int iVar12;
  int iVar13;
  int iVar14;
  ushort uVar15;
  uint uVar16;
  
  puVar5 = PTR_DAT_00045f58;
  puVar4 = PTR_DAT_00045f54;
  iVar14 = (int)DAT_00045f40;
  sVar2 = *(short *)PTR_Selection_ProposalLookupAxis_00045f48;
  sVar3 = *(short *)PTR_DAT_00045f4c;
  bVar1 = *PTR_DAT_00045f50;
  uVar16 = 0;
  do {
    puVar11 = (undefined2 *)((uVar16 & 0xff) * 0xc + iVar14);
    *puVar11 = 2;
    uVar10 = uVar16 & 0xff;
    puVar11[1] = 0;
    puVar11[2] = 0;
    uVar6 = SUB42(puVar5,0);
    puVar11[3] = uVar6;
    iVar9 = (uVar16 & 0xff) * 4;
    iVar12 = (uVar16 & 0xff) * 0xc + iVar14;
    if (param_1 == '\x01') {
      if (uVar10 < 5) {
        *(undefined2 *)(iVar12 + 8) = uVar6;
        *(undefined2 *)(iVar12 + 10) = uVar6;
        *(int *)(PTR_DAT_00045f5c + iVar9) = iVar12;
        uVar10 = uVar16 & 0xff;
        PTR_Selection_ThresholdOperations_00045f60[uVar10] = 5;
        puVar4[uVar10] = 6;
      }
      else {
        uVar10 = 4;
      }
    }
    else {
      if (uVar10 < 5) {
        sVar7 = (*(code *)PTR_Selection_CalculateOverlayLowerValue_00045f68)
                          (uVar16,(int)(char)-(((bVar1 & 8) == 0) + -1),
                           (int)*(short *)PTR_Selection_OverlayHistoryAxis_00045f64,
                           (int)(short)(sVar3 << 1));
        if ((*(byte *)(int)DAT_00045f42 & 1) == 1) {
          uVar15 = *(short *)(int)DAT_00045f44 + *(short *)PTR_DAT_00045f6c;
        }
        else {
          uVar15 = *(short *)PTR_DAT_00046014 + sVar7;
        }
        iVar12 = (uVar16 & 0xff) * 0x10;
        uVar8 = (*(code *)PTR_Lookup_InterpolateWordCurve_0004601c)
                          ((int)sVar2,PTR_Selection_OverlayWordCurves_200__00046018 + iVar12);
        if (*PTR_Selection_SourceCode_00046020 == '\x01') {
          uVar8 = (*(code *)PTR_Lookup_InterpolateWordCurve_0004601c)
                            ((int)sVar2,PTR_Selection_OverlayWordCurves_240__00046024 + iVar12);
        }
        if (uVar15 < uVar8) {
          uVar15 = uVar8;
        }
        iVar12 = (uVar16 & 0xff) * 0xc + iVar14;
        *(ushort *)(iVar12 + 8) = uVar15;
        *(ushort *)(iVar12 + 10) = uVar15;
        iVar13 = (uVar10 + 5) * 0xc + iVar14;
        *(short *)(iVar13 + 8) = sVar7;
        *(short *)(iVar13 + 10) = sVar7;
        *(int *)(PTR_DAT_00046028 + iVar9) = iVar12;
      }
      else {
        *(int *)(PTR_DAT_00046028 + iVar9) = iVar12;
      }
      uVar10 = uVar16 & 0xff;
      PTR_Selection_ThresholdOperations_0004602c[uVar10] = 5;
      puVar4[uVar10] = 6;
    }
    uVar16 = uVar16 + 1;
  } while ((uVar16 & 0xff) < 10);
  return uVar10;
}

