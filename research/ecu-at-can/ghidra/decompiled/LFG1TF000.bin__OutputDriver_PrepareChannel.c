/* Ghidra analysis output; verify against original SH instructions. */

/* 1basedinput; feedbacksignsticky, stocklookup/manual/diagnostictarget, signedworddelta88limiter,
   unsigned200..1000clamp.809Ezero/A620testoverridewins.1056cases+40edges/160chains.18A44handoffopen.
    */

void OutputDriver_PrepareChannel(int param_1)

{
  char cVar1;
  undefined *puVar2;
  short sVar3;
  undefined2 uVar4;
  undefined2 *puVar5;
  short sVar6;
  int iVar7;
  int iVar8;
  short *psVar9;
  uint uVar10;
  int iVar11;
  int iVar12;
  uint uVar13;
  undefined *puVar14;
  
  uVar13 = DAT_00052f82 + param_1;
  uVar10 = uVar13 & 0xff;
  if ((PTR_DAT_00052f88[uVar10] == '\0') &&
     (((int)*(short *)((uVar13 & 0xff) * 2 + (int)DAT_00052f84) & (uint)PTR_DAT_00052fa8) !=
      ((int)*(short *)((uVar13 & 0xff) * 2 + (int)DAT_00052f72) & (uint)PTR_DAT_00052fa8))) {
    PTR_DAT_00052f88[uVar10] = 1;
  }
  sVar6 = DAT_00052f86;
  iVar12 = (uVar13 & 0xff) * 2;
  iVar8 = (int)DAT_00052f86;
  iVar7 = (int)DAT_00052f70;
  *(undefined2 *)(DAT_00052f72 + iVar12) = *(undefined2 *)(iVar12 + DAT_00052f84);
  puVar2 = PTR_OutputDriver_CurrentWords_00052f8c;
  iVar7 = (*(code *)PTR_FUN_00052fac)
                    ((int)*(short *)(PTR_OutputDriver_CurrentWords_00052f8c + iVar12),iVar7,iVar8);
  if (*(char *)(uVar10 + (int)DAT_00052f6a) == '\0') {
    psVar9 = (short *)(PTR_OutputDriver_MappedWords_00052fb0 + iVar12);
    sVar3 = (*(code *)PTR_Lookup_UniformWordStep_00052fbc)
                      ((int)*(short *)(PTR_OutputRecord_ComputedWords_00052fb8 + iVar12),
                       *(undefined4 *)(PTR_PTR_00052fb4 + (uVar13 & 0xff) * 4),0x32);
    *psVar9 = sVar3;
    iVar11 = *psVar9 - iVar7;
    puVar14 = (undefined *)(int)*psVar9;
  }
  else {
    puVar14 = (undefined *)(int)*(short *)(iVar12 + DAT_0005309c);
    iVar11 = (int)puVar14 - iVar7;
  }
  if (*(char *)(int)DAT_0005309e != '\0') {
    puVar14 = (undefined *)(int)*(short *)(iVar12 + DAT_000530a0);
    iVar11 = (int)puVar14 - iVar7;
  }
  sVar3 = (*(code *)PTR_FUN_000530ac)(iVar11);
  if (0x58 < sVar3) {
    if ((short)iVar11 < 1) {
      puVar14 = PTR_DAT_000530b0 + iVar7;
    }
    else {
      puVar14 = (undefined *)(iVar7 + 0x58);
    }
  }
  iVar7 = (int)DAT_000530a2;
  puVar5 = (undefined2 *)(puVar2 + iVar12);
  *(undefined2 *)(PTR_OutputDriver_PreviousWords_000530b4 + iVar12) = *puVar5;
  uVar4 = (*DAT_000530b8)(puVar14,iVar7,iVar8);
  *puVar5 = uVar4;
  if ((CAN201_Word0Rescaled == 0) && (*(char *)(int)DAT_000530a4 != '\0')) {
    cVar1 = *(char *)(int)DAT_000530a4;
    if ((cVar1 != '\x01') &&
       ((sVar6 = DAT_000530a2, cVar1 != '\x02' && (sVar6 = DAT_000530a6, cVar1 != '\x03')))) {
      sVar6 = 100;
    }
    *(short *)(puVar2 + iVar12) = sVar6;
    *(short *)(PTR_OutputDriver_PreviousWords_000530b4 + iVar12) = sVar6;
  }
  return;
}

