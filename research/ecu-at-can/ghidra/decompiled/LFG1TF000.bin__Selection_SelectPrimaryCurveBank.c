/* Ghidra analysis output; verify against original SH instructions. */

/* Class8080=FF holds outputs; otherwise prioritizes9C7C bit0..3,9E88 dynamic copy,9B5C fixed
   bank,92D7/92CA/class6 and exactA534=1. Writes ten9AEC pointers/9B14 operations/9B32 kinds,9B40
   and9AEA/B flags.2560 stock cases; tcu-curve-sources.txt. */

undefined * Selection_SelectPrimaryCurveBank(void)

{
  bool bVar1;
  bool bVar2;
  undefined *puVar3;
  byte bVar6;
  byte bVar7;
  byte bVar8;
  byte bVar9;
  int iVar4;
  undefined *puVar5;
  undefined1 uVar10;
  undefined1 uVar11;
  undefined *puVar12;
  undefined1 uVar13;
  int iVar14;
  
  bVar9 = TransmissionStateClass;
  puVar5 = PTR_DAT_000471a4;
  puVar3 = PTR_DAT_000471a0;
  puVar12 = PTR_WORD_ARRAY_0004719c;
  bVar1 = ((int)(char)*PTR_DAT_00047190 & 0x80U) == 0;
  if (TransmissionStateClass == 0xff) {
    puVar5 = (undefined *)0xffffffff;
  }
  else {
    uVar11 = 0;
    uVar13 = 0;
    uVar10 = 0;
    bVar7 = *PTR_Request_CancellationFlags_00047194;
    bVar8 = *PTR_DAT_00047198;
    PTR_DAT_000471a0[1] = PTR_DAT_000471a0[1] | 1;
    if ((*puVar5 & 1) == 1) {
      uVar11 = 0xb;
      uVar13 = 8;
      uVar10 = 0xb;
      puVar12 = PTR_WORD_ARRAY_0007404c_720__000471a8;
    }
    if ((*puVar5 & 1) == 0) {
      bVar6 = puVar3[1] & 0xfd;
    }
    else {
      bVar6 = puVar3[1] | 2;
    }
    puVar3[1] = bVar6;
    if ((*puVar5 & 2) == 0) {
      bVar6 = puVar3[1] & 0xfb;
    }
    else {
      uVar11 = 0xc;
      uVar13 = 9;
      uVar10 = 0xc;
      bVar6 = puVar3[1] | 4;
      puVar12 = PTR_WORD_ARRAY_0007404c_960__000471ac;
    }
    puVar3[1] = bVar6;
    if ((*puVar5 & 4) == 0) {
      bVar6 = puVar3[1] & 0xf7;
    }
    else {
      uVar11 = 0xd;
      uVar13 = 10;
      uVar10 = 0xd;
      bVar6 = puVar3[1] | 8;
      puVar12 = PTR_WORD_ARRAY_0007404c_1200__000471b0;
    }
    puVar3[1] = bVar6;
    if ((*puVar5 & 8) == 0) {
      bVar6 = puVar3[1] & 0xef;
    }
    else {
      uVar11 = 0xe;
      uVar13 = 0xb;
      uVar10 = 0xe;
      bVar6 = puVar3[1] | 0x10;
      puVar12 = PTR_WORD_ARRAY_0007404c_1440__000471b4;
    }
    puVar3[1] = bVar6;
    if ((*PTR_DAT_000471b8 & 1) == 1) {
      (*(code *)PTR_Selection_CopyDynamicCurves_000471bc)();
      uVar11 = 1;
      uVar13 = 1;
      uVar10 = 1;
      puVar12 = PTR_DAT_000471c0;
    }
    if ((*PTR_DAT_000471b8 & 1) == 0) {
      bVar6 = puVar3[1] & 0xdf;
    }
    else {
      bVar6 = puVar3[1] | 0x20;
    }
    puVar3[1] = bVar6;
    bVar2 = false;
    if (((((bVar7 & 1) == 1) && ((bVar8 & 8) == 0)) && (*PTR_DAT_000471c4 == '\x01')) ||
       ((*PTR_DAT_000471c8 & 1) == 1)) {
      uVar10 = 3;
      uVar11 = 3;
      uVar13 = 2;
      bVar2 = true;
      puVar12 = PTR_WORD_ARRAY_0007404c_480__000471cc;
    }
    if (bVar2) {
      bVar7 = *puVar3 | 1;
    }
    else {
      bVar7 = *puVar3 & 0xfe;
    }
    *puVar3 = bVar7;
    bVar7 = *PTR_DAT_000471d0;
    bVar2 = false;
    if ((((bVar7 & 1) == 1) && (bVar1)) && (bVar9 == 6)) {
      uVar10 = 0xf;
      uVar13 = 0xc;
      uVar11 = 0xf;
      bVar2 = true;
      puVar12 = PTR_WORD_ARRAY_0007404c_1680__000471d4;
    }
    if (bVar2) {
      bVar8 = puVar3[1] | 0x40;
    }
    else {
      bVar8 = puVar3[1] & 0xbf;
    }
    puVar3[1] = bVar8;
    bVar2 = false;
    if ((((bVar7 & 1) == 1) && (*PTR_DAT_000471d8 == '\x01')) && ((bVar1 && (bVar9 == 6)))) {
      uVar10 = 0x10;
      uVar11 = 0x10;
      uVar13 = 0xd;
      bVar2 = true;
      puVar12 = PTR_WORD_ARRAY_0007404c_1920__000471dc;
    }
    if (bVar2) {
      bVar9 = puVar3[1] | 0x80;
    }
    else {
      bVar9 = puVar3[1] & 0x7f;
    }
    puVar3[1] = bVar9;
    iVar14 = 0;
    *PTR_Selection_SourceCode_0004722c = uVar10;
    puVar3 = PTR_DAT_00047230;
    do {
      iVar4 = (*(code *)PTR_Arithmetic_SaturatingMultiplyShift_00047234)(iVar14,0x18,0);
      *(undefined **)(puVar3 + iVar14 * 4) = puVar12 + iVar4 * 2;
      PTR_Selection_ThresholdOperations_00047238[iVar14] = uVar11;
      puVar5 = PTR_DAT_0004723c;
      PTR_DAT_0004723c[iVar14] = uVar13;
      iVar14 = iVar14 + 1;
    } while (iVar14 < 10);
  }
  return puVar5;
}

