/* Ghidra analysis output; verify against original SH instructions. */

/* Original signed division returns saturated Q16 ratio, including zero denominator behavior.77
   boundary/sign cases with composed arithmetic interpreter. */

undefined8 Arithmetic_SaturatingSignedQ16Divide(uint param_1,int param_2)

{
  bool bVar1;
  char cVar2;
  bool bVar3;
  bool bVar4;
  uint uVar5;
  uint in_r1;
  undefined *puVar6;
  uint uVar7;
  uint uVar8;
  uint uVar9;
  uint uVar11;
  uint uVar12;
  uint uVar14;
  int iVar15;
  uint uVar16;
  uint uVar17;
  uint uVar18;
  uint uVar19;
  uint uVar20;
  uint uVar21;
  uint uVar22;
  uint uVar23;
  uint uVar24;
  uint uVar25;
  uint uVar26;
  uint uVar27;
  uint uVar28;
  uint uVar29;
  uint uVar30;
  uint uVar31;
  uint uVar32;
  uint uVar33;
  uint uVar34;
  uint uVar35;
  uint uVar36;
  uint uVar37;
  uint uVar38;
  uint uVar39;
  uint uVar40;
  uint uVar41;
  uint uVar42;
  uint uVar43;
  uint uVar44;
  uint uVar10;
  uint uVar13;
  
  uVar5 = 0;
  if (param_1 != 0) {
    if (param_2 == 0) {
      uVar5 = DAT_000022dc + ((param_1 & 0x80000000) != 0);
      in_r1 = DAT_000022dc;
    }
    else if (((DAT_000022dc & param_1) != 0) ||
            (in_r1 = 0xffffffff, uVar5 = DAT_000022dc, param_2 != -1)) {
      uVar7 = -(uint)((param_1 & 0x80000000) != 0);
      uVar14 = param_1 - ((uVar7 & 0x80000000) != 0);
      uVar7 = uVar7 - (param_1 < uVar14);
      bVar1 = param_2 < 0;
      uVar5 = (uint)bVar1 << 9;
      uVar12 = uVar14 * 2;
      uVar14 = uVar7 * 2 | (uint)((uVar14 & 0x80000000) != 0);
      bVar3 = (int)uVar7 < 0 == bVar1;
      bVar4 = bVar1 == ((uVar7 & 0x80000000) != 0);
      uVar8 = (uint)bVar3 * (uVar14 - param_2) + (uint)!bVar3 * (uVar14 + param_2);
      cVar2 = bVar3 * (uVar14 < uVar8) + !bVar3 * (uVar8 < uVar14);
      uVar14 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
      uVar13 = uVar5 | uVar14;
      uVar9 = uVar8 * 2 | (uint)((uVar12 & 0x80000000) != 0);
      bVar3 = ((byte)(uVar13 >> 8) & 1) == ((byte)(uVar13 >> 9) & 1);
      bVar4 = (bool)((byte)(uVar13 >> 9) & 1) == ((uVar8 & 0x80000000) != 0);
      uVar10 = (uint)bVar3 * (uVar9 - param_2) + (uint)!bVar3 * (uVar9 + param_2);
      cVar2 = bVar3 * (uVar9 < uVar10) + !bVar3 * (uVar10 < uVar9);
      uVar13 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
      uVar16 = uVar5 | uVar14 & 0xfffffeff | uVar13;
      uVar9 = uVar5 | uVar14 & 0xfffffefe;
      uVar8 = uVar9 | uVar13;
      uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x40000000) != 0);
      bVar3 = ((byte)(uVar8 >> 8) & 1) == ((byte)(uVar8 >> 9) & 1);
      bVar4 = (bool)((byte)(uVar8 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
      uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
      cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
      uVar8 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
      uVar17 = uVar9 | uVar13 & 0xfffffeff | uVar8;
      uVar9 = uVar9 | uVar13 & 0xfffffefe;
      uVar13 = uVar9 | uVar8;
      uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x20000000) != 0);
      bVar3 = ((byte)(uVar13 >> 8) & 1) == ((byte)(uVar13 >> 9) & 1);
      bVar4 = (bool)((byte)(uVar13 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
      uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
      cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
      uVar13 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
      uVar18 = uVar9 | uVar8 & 0xfffffeff | uVar13;
      uVar9 = uVar9 | uVar8 & 0xfffffefe;
      uVar8 = uVar9 | uVar13;
      uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x10000000) != 0);
      bVar3 = ((byte)(uVar8 >> 8) & 1) == ((byte)(uVar8 >> 9) & 1);
      bVar4 = (bool)((byte)(uVar8 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
      uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
      cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
      uVar8 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
      uVar19 = uVar9 | uVar13 & 0xfffffeff | uVar8;
      uVar9 = uVar9 | uVar13 & 0xfffffefe;
      uVar13 = uVar9 | uVar8;
      uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x8000000) != 0);
      bVar3 = ((byte)(uVar13 >> 8) & 1) == ((byte)(uVar13 >> 9) & 1);
      bVar4 = (bool)((byte)(uVar13 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
      uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
      cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
      uVar13 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
      uVar20 = uVar9 | uVar8 & 0xfffffeff | uVar13;
      uVar9 = uVar9 | uVar8 & 0xfffffefe;
      uVar8 = uVar9 | uVar13;
      uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x4000000) != 0);
      bVar3 = ((byte)(uVar8 >> 8) & 1) == ((byte)(uVar8 >> 9) & 1);
      bVar4 = (bool)((byte)(uVar8 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
      uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
      cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
      uVar8 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
      uVar21 = uVar9 | uVar13 & 0xfffffeff | uVar8;
      uVar9 = uVar9 | uVar13 & 0xfffffefe;
      uVar13 = uVar9 | uVar8;
      uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x2000000) != 0);
      bVar3 = ((byte)(uVar13 >> 8) & 1) == ((byte)(uVar13 >> 9) & 1);
      bVar4 = (bool)((byte)(uVar13 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
      uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
      cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
      uVar13 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
      uVar22 = uVar9 | uVar8 & 0xfffffeff | uVar13;
      uVar9 = uVar9 | uVar8 & 0xfffffefe;
      uVar8 = uVar9 | uVar13;
      uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x1000000) != 0);
      bVar3 = ((byte)(uVar8 >> 8) & 1) == ((byte)(uVar8 >> 9) & 1);
      bVar4 = (bool)((byte)(uVar8 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
      uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
      cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
      uVar8 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
      uVar23 = uVar9 | uVar13 & 0xfffffeff | uVar8;
      uVar9 = uVar9 | uVar13 & 0xfffffefe;
      uVar13 = uVar9 | uVar8;
      uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x800000) != 0);
      bVar3 = ((byte)(uVar13 >> 8) & 1) == ((byte)(uVar13 >> 9) & 1);
      bVar4 = (bool)((byte)(uVar13 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
      uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
      cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
      uVar13 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
      uVar24 = uVar9 | uVar8 & 0xfffffeff | uVar13;
      uVar9 = uVar9 | uVar8 & 0xfffffefe;
      uVar8 = uVar9 | uVar13;
      uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x400000) != 0);
      bVar3 = ((byte)(uVar8 >> 8) & 1) == ((byte)(uVar8 >> 9) & 1);
      bVar4 = (bool)((byte)(uVar8 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
      uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
      cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
      uVar8 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
      uVar25 = uVar9 | uVar13 & 0xfffffeff | uVar8;
      uVar9 = uVar9 | uVar13 & 0xfffffefe;
      uVar13 = uVar9 | uVar8;
      uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x200000) != 0);
      bVar3 = ((byte)(uVar13 >> 8) & 1) == ((byte)(uVar13 >> 9) & 1);
      bVar4 = (bool)((byte)(uVar13 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
      uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
      cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
      uVar13 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
      uVar26 = uVar9 | uVar8 & 0xfffffeff | uVar13;
      uVar9 = uVar9 | uVar8 & 0xfffffefe;
      uVar8 = uVar9 | uVar13;
      uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x100000) != 0);
      bVar3 = ((byte)(uVar8 >> 8) & 1) == ((byte)(uVar8 >> 9) & 1);
      bVar4 = (bool)((byte)(uVar8 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
      uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
      cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
      uVar8 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
      uVar27 = uVar9 | uVar13 & 0xfffffeff | uVar8;
      uVar9 = uVar9 | uVar13 & 0xfffffefe;
      uVar13 = uVar9 | uVar8;
      uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x80000) != 0);
      bVar3 = ((byte)(uVar13 >> 8) & 1) == ((byte)(uVar13 >> 9) & 1);
      bVar4 = (bool)((byte)(uVar13 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
      uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
      cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
      uVar13 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
      uVar28 = uVar9 | uVar8 & 0xfffffeff | uVar13;
      uVar9 = uVar9 | uVar8 & 0xfffffefe;
      uVar8 = uVar9 | uVar13;
      uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x40000) != 0);
      bVar3 = ((byte)(uVar8 >> 8) & 1) == ((byte)(uVar8 >> 9) & 1);
      bVar4 = (bool)((byte)(uVar8 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
      uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
      cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
      uVar8 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
      uVar29 = uVar9 | uVar13 & 0xfffffeff | uVar8;
      uVar9 = uVar9 | uVar13 & 0xfffffefe;
      uVar13 = uVar9 | uVar8;
      uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x20000) != 0);
      bVar3 = ((byte)(uVar13 >> 8) & 1) == ((byte)(uVar13 >> 9) & 1);
      bVar4 = (bool)((byte)(uVar13 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
      uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
      cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
      uVar13 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
      uVar30 = uVar9 | uVar8 & 0xfffffeff | uVar13;
      uVar9 = uVar9 | uVar8 & 0xfffffefe;
      uVar8 = uVar9 | uVar13;
      uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x10000) != 0);
      bVar3 = ((byte)(uVar8 >> 8) & 1) == ((byte)(uVar8 >> 9) & 1);
      bVar4 = (bool)((byte)(uVar8 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
      uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
      cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
      uVar8 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
      uVar31 = uVar9 | uVar13 & 0xfffffeff | uVar8;
      uVar9 = uVar9 | uVar13 & 0xfffffefe;
      uVar13 = uVar9 | uVar8;
      uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x8000) != 0);
      bVar3 = ((byte)(uVar13 >> 8) & 1) == ((byte)(uVar13 >> 9) & 1);
      bVar4 = (bool)((byte)(uVar13 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
      uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
      cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
      uVar13 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
      uVar32 = uVar9 | uVar8 & 0xfffffeff | uVar13;
      uVar9 = uVar9 | uVar8 & 0xfffffefe;
      uVar8 = uVar9 | uVar13;
      uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x4000) != 0);
      bVar3 = ((byte)(uVar8 >> 8) & 1) == ((byte)(uVar8 >> 9) & 1);
      bVar4 = (bool)((byte)(uVar8 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
      uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
      cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
      uVar8 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
      uVar33 = uVar9 | uVar13 & 0xfffffeff | uVar8;
      uVar9 = uVar9 | uVar13 & 0xfffffefe;
      uVar13 = uVar9 | uVar8;
      uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x2000) != 0);
      bVar3 = ((byte)(uVar13 >> 8) & 1) == ((byte)(uVar13 >> 9) & 1);
      bVar4 = (bool)((byte)(uVar13 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
      uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
      cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
      uVar13 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
      uVar34 = uVar9 | uVar8 & 0xfffffeff | uVar13;
      uVar9 = uVar9 | uVar8 & 0xfffffefe;
      uVar8 = uVar9 | uVar13;
      uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x1000) != 0);
      bVar3 = ((byte)(uVar8 >> 8) & 1) == ((byte)(uVar8 >> 9) & 1);
      bVar4 = (bool)((byte)(uVar8 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
      uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
      cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
      uVar8 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
      uVar35 = uVar9 | uVar13 & 0xfffffeff | uVar8;
      uVar9 = uVar9 | uVar13 & 0xfffffefe;
      uVar13 = uVar9 | uVar8;
      uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x800) != 0);
      bVar3 = ((byte)(uVar13 >> 8) & 1) == ((byte)(uVar13 >> 9) & 1);
      bVar4 = (bool)((byte)(uVar13 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
      uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
      cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
      uVar13 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
      uVar36 = uVar9 | uVar8 & 0xfffffeff | uVar13;
      uVar9 = uVar9 | uVar8 & 0xfffffefe;
      uVar8 = uVar9 | uVar13;
      uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x400) != 0);
      bVar3 = ((byte)(uVar8 >> 8) & 1) == ((byte)(uVar8 >> 9) & 1);
      bVar4 = (bool)((byte)(uVar8 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
      uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
      cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
      uVar8 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
      uVar37 = uVar9 | uVar13 & 0xfffffeff | uVar8;
      uVar9 = uVar9 | uVar13 & 0xfffffefe;
      uVar13 = uVar9 | uVar8;
      uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x200) != 0);
      bVar3 = ((byte)(uVar13 >> 8) & 1) == ((byte)(uVar13 >> 9) & 1);
      bVar4 = (bool)((byte)(uVar13 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
      uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
      cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
      uVar13 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
      uVar38 = uVar9 | uVar8 & 0xfffffeff | uVar13;
      uVar9 = uVar9 | uVar8 & 0xfffffefe;
      uVar8 = uVar9 | uVar13;
      uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x100) != 0);
      bVar3 = ((byte)(uVar8 >> 8) & 1) == ((byte)(uVar8 >> 9) & 1);
      bVar4 = (bool)((byte)(uVar8 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
      uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
      cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
      uVar8 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
      uVar39 = uVar9 | uVar13 & 0xfffffeff | uVar8;
      uVar9 = uVar9 | uVar13 & 0xfffffefe;
      uVar13 = uVar9 | uVar8;
      uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x80) != 0);
      bVar3 = ((byte)(uVar13 >> 8) & 1) == ((byte)(uVar13 >> 9) & 1);
      bVar4 = (bool)((byte)(uVar13 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
      uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
      cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
      uVar13 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
      uVar40 = uVar9 | uVar8 & 0xfffffeff | uVar13;
      uVar9 = uVar9 | uVar8 & 0xfffffefe;
      uVar8 = uVar9 | uVar13;
      uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x40) != 0);
      bVar3 = ((byte)(uVar8 >> 8) & 1) == ((byte)(uVar8 >> 9) & 1);
      bVar4 = (bool)((byte)(uVar8 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
      uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
      cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
      uVar8 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
      uVar41 = uVar9 | uVar13 & 0xfffffeff | uVar8;
      uVar9 = uVar9 | uVar13 & 0xfffffefe;
      uVar13 = uVar9 | uVar8;
      uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x20) != 0);
      bVar3 = ((byte)(uVar13 >> 8) & 1) == ((byte)(uVar13 >> 9) & 1);
      bVar4 = (bool)((byte)(uVar13 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
      uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
      cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
      uVar13 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
      uVar42 = uVar9 | uVar8 & 0xfffffeff | uVar13;
      uVar9 = uVar9 | uVar8 & 0xfffffefe;
      uVar8 = uVar9 | uVar13;
      uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x10) != 0);
      bVar3 = ((byte)(uVar8 >> 8) & 1) == ((byte)(uVar8 >> 9) & 1);
      bVar4 = (bool)((byte)(uVar8 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
      uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
      cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
      uVar8 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
      uVar43 = uVar9 | uVar13 & 0xfffffeff | uVar8;
      uVar9 = uVar9 | uVar13 & 0xfffffefe;
      uVar13 = uVar9 | uVar8;
      uVar11 = uVar10 * 2 | (uint)((uVar12 & 8) != 0);
      bVar3 = ((byte)(uVar13 >> 8) & 1) == ((byte)(uVar13 >> 9) & 1);
      bVar4 = (bool)((byte)(uVar13 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
      uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
      cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
      uVar13 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
      uVar44 = uVar9 | uVar8 & 0xfffffeff | uVar13;
      uVar9 = uVar9 | uVar8 & 0xfffffefe;
      uVar8 = uVar9 | uVar13;
      uVar11 = uVar10 * 2 | (uint)((uVar12 & 4) != 0);
      bVar3 = ((byte)(uVar8 >> 8) & 1) == ((byte)(uVar8 >> 9) & 1);
      bVar4 = (bool)((byte)(uVar8 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
      uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
      cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
      uVar8 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
      uVar11 = uVar9 | uVar13 & 0xfffffeff | uVar8;
      uVar9 = uVar9 | uVar13 & 0xfffffefe;
      uVar13 = uVar9 | uVar8;
      uVar12 = uVar10 * 2 | (uint)((uVar12 & 2) != 0);
      bVar3 = ((byte)(uVar13 >> 8) & 1) == ((byte)(uVar13 >> 9) & 1);
      bVar4 = (bool)((byte)(uVar13 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
      uVar13 = (uint)bVar3 * (uVar12 - param_2) + (uint)!bVar3 * (uVar12 + param_2);
      cVar2 = bVar3 * (uVar12 < uVar13) + !bVar3 * (uVar13 < uVar12);
      uVar13 = uVar9 | uVar8 & 0xfffffeff |
               (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
      iVar15 = ((((((((((((((((((((((((((((((((uint)(((byte)((uVar5 | uVar14) >> 8) & 1) ==
                                                    ((byte)((uVar5 | uVar14) >> 9) & 1)) << 1 |
                                             (uint)(((byte)(uVar16 >> 8) & 1) ==
                                                   ((byte)(uVar16 >> 9) & 1))) << 1 |
                                            (uint)(((byte)(uVar17 >> 8) & 1) ==
                                                  ((byte)(uVar17 >> 9) & 1))) << 1 |
                                           (uint)(((byte)(uVar18 >> 8) & 1) ==
                                                 ((byte)(uVar18 >> 9) & 1))) << 1 |
                                          (uint)(((byte)(uVar19 >> 8) & 1) ==
                                                ((byte)(uVar19 >> 9) & 1))) << 1 |
                                         (uint)(((byte)(uVar20 >> 8) & 1) ==
                                               ((byte)(uVar20 >> 9) & 1))) << 1 |
                                        (uint)(((byte)(uVar21 >> 8) & 1) ==
                                              ((byte)(uVar21 >> 9) & 1))) << 1 |
                                       (uint)(((byte)(uVar22 >> 8) & 1) == ((byte)(uVar22 >> 9) & 1)
                                             )) << 1 |
                                      (uint)(((byte)(uVar23 >> 8) & 1) == ((byte)(uVar23 >> 9) & 1))
                                      ) << 1 | (uint)(((byte)(uVar24 >> 8) & 1) ==
                                                     ((byte)(uVar24 >> 9) & 1))) << 1 |
                                    (uint)(((byte)(uVar25 >> 8) & 1) == ((byte)(uVar25 >> 9) & 1)))
                                    << 1 | (uint)(((byte)(uVar26 >> 8) & 1) ==
                                                 ((byte)(uVar26 >> 9) & 1))) << 1 |
                                  (uint)(((byte)(uVar27 >> 8) & 1) == ((byte)(uVar27 >> 9) & 1))) <<
                                  1 | (uint)(((byte)(uVar28 >> 8) & 1) == ((byte)(uVar28 >> 9) & 1))
                                 ) << 1 | (uint)(((byte)(uVar29 >> 8) & 1) ==
                                                ((byte)(uVar29 >> 9) & 1))) << 1 |
                               (uint)(((byte)(uVar30 >> 8) & 1) == ((byte)(uVar30 >> 9) & 1))) << 1
                              | (uint)(((byte)(uVar31 >> 8) & 1) == ((byte)(uVar31 >> 9) & 1))) << 1
                             | (uint)(((byte)(uVar32 >> 8) & 1) == ((byte)(uVar32 >> 9) & 1))) << 1
                            | (uint)(((byte)(uVar33 >> 8) & 1) == ((byte)(uVar33 >> 9) & 1))) << 1 |
                           (uint)(((byte)(uVar34 >> 8) & 1) == ((byte)(uVar34 >> 9) & 1))) << 1 |
                          (uint)(((byte)(uVar35 >> 8) & 1) == ((byte)(uVar35 >> 9) & 1))) << 1 |
                         (uint)(((byte)(uVar36 >> 8) & 1) == ((byte)(uVar36 >> 9) & 1))) << 1 |
                        (uint)(((byte)(uVar37 >> 8) & 1) == ((byte)(uVar37 >> 9) & 1))) << 1 |
                       (uint)(((byte)(uVar38 >> 8) & 1) == ((byte)(uVar38 >> 9) & 1))) << 1 |
                      (uint)(((byte)(uVar39 >> 8) & 1) == ((byte)(uVar39 >> 9) & 1))) << 1 |
                     (uint)(((byte)(uVar40 >> 8) & 1) == ((byte)(uVar40 >> 9) & 1))) << 1 |
                    (uint)(((byte)(uVar41 >> 8) & 1) == ((byte)(uVar41 >> 9) & 1))) << 1 |
                   (uint)(((byte)(uVar42 >> 8) & 1) == ((byte)(uVar42 >> 9) & 1))) << 1 |
                  (uint)(((byte)(uVar43 >> 8) & 1) == ((byte)(uVar43 >> 9) & 1))) << 1 |
                 (uint)(((byte)(uVar44 >> 8) & 1) == ((byte)(uVar44 >> 9) & 1))) << 1 |
                (uint)(((byte)(uVar11 >> 8) & 1) == ((byte)(uVar11 >> 9) & 1))) << 1 |
               (uint)(((byte)(uVar13 >> 8) & 1) == ((byte)(uVar13 >> 9) & 1))) +
               (uint)(bVar1 != (int)uVar7 < 0);
      uVar5 = DAT_000022dc;
      puVar6 = PTR_LAB_00007ffe_1_000022e0;
      if (iVar15 <= (int)PTR_LAB_00007ffe_1_000022e0) {
        uVar5 = ~DAT_000022dc;
        puVar6 = (undefined *)~(uint)PTR_LAB_00007ffe_1_000022e0;
        if ((int)puVar6 <= iVar15) {
          puVar6 = (undefined *)(param_1 << 1);
          uVar5 = (uint)((param_1 & 0x80000000) != 0) * -2;
          uVar14 = param_1 * 0x10000 - (uint)((uVar5 & 0x10000) != 0);
          uVar9 = ((((((((((((((((uVar5 | (param_1 & 0x80000000) != 0) << 1 |
                                (uint)((param_1 & 0x40000000) != 0)) << 1 |
                               (uint)((param_1 & 0x20000000) != 0)) << 1 |
                              (uint)((param_1 & 0x10000000) != 0)) << 1 |
                             (uint)((param_1 & 0x8000000) != 0)) << 1 |
                            (uint)((param_1 & 0x4000000) != 0)) << 1 |
                           (uint)((param_1 & 0x2000000) != 0)) << 1 |
                          (uint)((param_1 & 0x1000000) != 0)) << 1 |
                         (uint)((param_1 & 0x800000) != 0)) << 1 | (uint)((param_1 & 0x400000) != 0)
                        ) << 1 | (uint)((param_1 & 0x200000) != 0)) << 1 |
                      (uint)((param_1 & 0x100000) != 0)) << 1 | (uint)((param_1 & 0x80000) != 0)) <<
                     1 | (uint)((param_1 & 0x40000) != 0)) << 1 | (uint)((param_1 & 0x20000) != 0))
                   << 1 | (uint)((param_1 & 0x10000) != 0)) - (uint)(param_1 * 0x10000 < uVar14);
          bVar1 = param_2 < 0;
          uVar5 = (uint)bVar1 << 9;
          uVar12 = uVar14 * 2;
          uVar14 = uVar9 * 2 | (uint)((uVar14 & 0x80000000) != 0);
          bVar3 = (int)uVar9 < 0 == bVar1;
          bVar4 = bVar1 == ((uVar9 & 0x80000000) != 0);
          uVar8 = (uint)bVar3 * (uVar14 - param_2) + (uint)!bVar3 * (uVar14 + param_2);
          cVar2 = bVar3 * (uVar14 < uVar8) + !bVar3 * (uVar8 < uVar14);
          uVar14 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
          uVar13 = uVar5 | uVar14;
          uVar7 = uVar8 * 2 | (uint)((uVar12 & 0x80000000) != 0);
          bVar3 = ((byte)(uVar13 >> 8) & 1) == ((byte)(uVar13 >> 9) & 1);
          bVar4 = (bool)((byte)(uVar13 >> 9) & 1) == ((uVar8 & 0x80000000) != 0);
          uVar10 = (uint)bVar3 * (uVar7 - param_2) + (uint)!bVar3 * (uVar7 + param_2);
          cVar2 = bVar3 * (uVar7 < uVar10) + !bVar3 * (uVar10 < uVar7);
          uVar13 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
          uVar16 = uVar5 | uVar14 & 0xfffffeff | uVar13;
          uVar7 = uVar5 | uVar14 & 0xfffffefe;
          uVar8 = uVar7 | uVar13;
          uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x40000000) != 0);
          bVar3 = ((byte)(uVar8 >> 8) & 1) == ((byte)(uVar8 >> 9) & 1);
          bVar4 = (bool)((byte)(uVar8 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
          uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
          cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
          uVar8 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
          uVar17 = uVar7 | uVar13 & 0xfffffeff | uVar8;
          uVar7 = uVar7 | uVar13 & 0xfffffefe;
          uVar13 = uVar7 | uVar8;
          uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x20000000) != 0);
          bVar3 = ((byte)(uVar13 >> 8) & 1) == ((byte)(uVar13 >> 9) & 1);
          bVar4 = (bool)((byte)(uVar13 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
          uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
          cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
          uVar13 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
          uVar18 = uVar7 | uVar8 & 0xfffffeff | uVar13;
          uVar7 = uVar7 | uVar8 & 0xfffffefe;
          uVar8 = uVar7 | uVar13;
          uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x10000000) != 0);
          bVar3 = ((byte)(uVar8 >> 8) & 1) == ((byte)(uVar8 >> 9) & 1);
          bVar4 = (bool)((byte)(uVar8 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
          uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
          cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
          uVar8 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
          uVar19 = uVar7 | uVar13 & 0xfffffeff | uVar8;
          uVar7 = uVar7 | uVar13 & 0xfffffefe;
          uVar13 = uVar7 | uVar8;
          uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x8000000) != 0);
          bVar3 = ((byte)(uVar13 >> 8) & 1) == ((byte)(uVar13 >> 9) & 1);
          bVar4 = (bool)((byte)(uVar13 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
          uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
          cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
          uVar13 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
          uVar20 = uVar7 | uVar8 & 0xfffffeff | uVar13;
          uVar7 = uVar7 | uVar8 & 0xfffffefe;
          uVar8 = uVar7 | uVar13;
          uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x4000000) != 0);
          bVar3 = ((byte)(uVar8 >> 8) & 1) == ((byte)(uVar8 >> 9) & 1);
          bVar4 = (bool)((byte)(uVar8 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
          uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
          cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
          uVar8 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
          uVar21 = uVar7 | uVar13 & 0xfffffeff | uVar8;
          uVar7 = uVar7 | uVar13 & 0xfffffefe;
          uVar13 = uVar7 | uVar8;
          uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x2000000) != 0);
          bVar3 = ((byte)(uVar13 >> 8) & 1) == ((byte)(uVar13 >> 9) & 1);
          bVar4 = (bool)((byte)(uVar13 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
          uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
          cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
          uVar13 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
          uVar22 = uVar7 | uVar8 & 0xfffffeff | uVar13;
          uVar7 = uVar7 | uVar8 & 0xfffffefe;
          uVar8 = uVar7 | uVar13;
          uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x1000000) != 0);
          bVar3 = ((byte)(uVar8 >> 8) & 1) == ((byte)(uVar8 >> 9) & 1);
          bVar4 = (bool)((byte)(uVar8 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
          uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
          cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
          uVar8 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
          uVar23 = uVar7 | uVar13 & 0xfffffeff | uVar8;
          uVar7 = uVar7 | uVar13 & 0xfffffefe;
          uVar13 = uVar7 | uVar8;
          uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x800000) != 0);
          bVar3 = ((byte)(uVar13 >> 8) & 1) == ((byte)(uVar13 >> 9) & 1);
          bVar4 = (bool)((byte)(uVar13 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
          uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
          cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
          uVar13 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
          uVar24 = uVar7 | uVar8 & 0xfffffeff | uVar13;
          uVar7 = uVar7 | uVar8 & 0xfffffefe;
          uVar8 = uVar7 | uVar13;
          uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x400000) != 0);
          bVar3 = ((byte)(uVar8 >> 8) & 1) == ((byte)(uVar8 >> 9) & 1);
          bVar4 = (bool)((byte)(uVar8 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
          uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
          cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
          uVar8 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
          uVar25 = uVar7 | uVar13 & 0xfffffeff | uVar8;
          uVar7 = uVar7 | uVar13 & 0xfffffefe;
          uVar13 = uVar7 | uVar8;
          uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x200000) != 0);
          bVar3 = ((byte)(uVar13 >> 8) & 1) == ((byte)(uVar13 >> 9) & 1);
          bVar4 = (bool)((byte)(uVar13 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
          uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
          cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
          uVar13 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
          uVar26 = uVar7 | uVar8 & 0xfffffeff | uVar13;
          uVar7 = uVar7 | uVar8 & 0xfffffefe;
          uVar8 = uVar7 | uVar13;
          uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x100000) != 0);
          bVar3 = ((byte)(uVar8 >> 8) & 1) == ((byte)(uVar8 >> 9) & 1);
          bVar4 = (bool)((byte)(uVar8 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
          uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
          cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
          uVar8 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
          uVar27 = uVar7 | uVar13 & 0xfffffeff | uVar8;
          uVar7 = uVar7 | uVar13 & 0xfffffefe;
          uVar13 = uVar7 | uVar8;
          uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x80000) != 0);
          bVar3 = ((byte)(uVar13 >> 8) & 1) == ((byte)(uVar13 >> 9) & 1);
          bVar4 = (bool)((byte)(uVar13 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
          uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
          cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
          uVar13 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
          uVar28 = uVar7 | uVar8 & 0xfffffeff | uVar13;
          uVar7 = uVar7 | uVar8 & 0xfffffefe;
          uVar8 = uVar7 | uVar13;
          uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x40000) != 0);
          bVar3 = ((byte)(uVar8 >> 8) & 1) == ((byte)(uVar8 >> 9) & 1);
          bVar4 = (bool)((byte)(uVar8 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
          uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
          cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
          uVar8 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
          uVar29 = uVar7 | uVar13 & 0xfffffeff | uVar8;
          uVar7 = uVar7 | uVar13 & 0xfffffefe;
          uVar13 = uVar7 | uVar8;
          uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x20000) != 0);
          bVar3 = ((byte)(uVar13 >> 8) & 1) == ((byte)(uVar13 >> 9) & 1);
          bVar4 = (bool)((byte)(uVar13 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
          uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
          cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
          uVar13 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
          uVar30 = uVar7 | uVar8 & 0xfffffeff | uVar13;
          uVar7 = uVar7 | uVar8 & 0xfffffefe;
          uVar8 = uVar7 | uVar13;
          uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x10000) != 0);
          bVar3 = ((byte)(uVar8 >> 8) & 1) == ((byte)(uVar8 >> 9) & 1);
          bVar4 = (bool)((byte)(uVar8 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
          uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
          cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
          uVar8 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
          uVar31 = uVar7 | uVar13 & 0xfffffeff | uVar8;
          uVar7 = uVar7 | uVar13 & 0xfffffefe;
          uVar13 = uVar7 | uVar8;
          uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x8000) != 0);
          bVar3 = ((byte)(uVar13 >> 8) & 1) == ((byte)(uVar13 >> 9) & 1);
          bVar4 = (bool)((byte)(uVar13 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
          uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
          cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
          uVar13 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
          uVar32 = uVar7 | uVar8 & 0xfffffeff | uVar13;
          uVar7 = uVar7 | uVar8 & 0xfffffefe;
          uVar8 = uVar7 | uVar13;
          uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x4000) != 0);
          bVar3 = ((byte)(uVar8 >> 8) & 1) == ((byte)(uVar8 >> 9) & 1);
          bVar4 = (bool)((byte)(uVar8 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
          uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
          cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
          uVar8 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
          uVar33 = uVar7 | uVar13 & 0xfffffeff | uVar8;
          uVar7 = uVar7 | uVar13 & 0xfffffefe;
          uVar13 = uVar7 | uVar8;
          uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x2000) != 0);
          bVar3 = ((byte)(uVar13 >> 8) & 1) == ((byte)(uVar13 >> 9) & 1);
          bVar4 = (bool)((byte)(uVar13 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
          uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
          cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
          uVar13 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
          uVar34 = uVar7 | uVar8 & 0xfffffeff | uVar13;
          uVar7 = uVar7 | uVar8 & 0xfffffefe;
          uVar8 = uVar7 | uVar13;
          uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x1000) != 0);
          bVar3 = ((byte)(uVar8 >> 8) & 1) == ((byte)(uVar8 >> 9) & 1);
          bVar4 = (bool)((byte)(uVar8 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
          uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
          cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
          uVar8 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
          uVar35 = uVar7 | uVar13 & 0xfffffeff | uVar8;
          uVar7 = uVar7 | uVar13 & 0xfffffefe;
          uVar13 = uVar7 | uVar8;
          uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x800) != 0);
          bVar3 = ((byte)(uVar13 >> 8) & 1) == ((byte)(uVar13 >> 9) & 1);
          bVar4 = (bool)((byte)(uVar13 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
          uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
          cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
          uVar13 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
          uVar36 = uVar7 | uVar8 & 0xfffffeff | uVar13;
          uVar7 = uVar7 | uVar8 & 0xfffffefe;
          uVar8 = uVar7 | uVar13;
          uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x400) != 0);
          bVar3 = ((byte)(uVar8 >> 8) & 1) == ((byte)(uVar8 >> 9) & 1);
          bVar4 = (bool)((byte)(uVar8 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
          uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
          cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
          uVar8 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
          uVar37 = uVar7 | uVar13 & 0xfffffeff | uVar8;
          uVar7 = uVar7 | uVar13 & 0xfffffefe;
          uVar13 = uVar7 | uVar8;
          uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x200) != 0);
          bVar3 = ((byte)(uVar13 >> 8) & 1) == ((byte)(uVar13 >> 9) & 1);
          bVar4 = (bool)((byte)(uVar13 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
          uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
          cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
          uVar13 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
          uVar38 = uVar7 | uVar8 & 0xfffffeff | uVar13;
          uVar7 = uVar7 | uVar8 & 0xfffffefe;
          uVar8 = uVar7 | uVar13;
          uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x100) != 0);
          bVar3 = ((byte)(uVar8 >> 8) & 1) == ((byte)(uVar8 >> 9) & 1);
          bVar4 = (bool)((byte)(uVar8 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
          uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
          cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
          uVar8 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
          uVar39 = uVar7 | uVar13 & 0xfffffeff | uVar8;
          uVar7 = uVar7 | uVar13 & 0xfffffefe;
          uVar13 = uVar7 | uVar8;
          uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x80) != 0);
          bVar3 = ((byte)(uVar13 >> 8) & 1) == ((byte)(uVar13 >> 9) & 1);
          bVar4 = (bool)((byte)(uVar13 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
          uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
          cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
          uVar13 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
          uVar40 = uVar7 | uVar8 & 0xfffffeff | uVar13;
          uVar7 = uVar7 | uVar8 & 0xfffffefe;
          uVar8 = uVar7 | uVar13;
          uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x40) != 0);
          bVar3 = ((byte)(uVar8 >> 8) & 1) == ((byte)(uVar8 >> 9) & 1);
          bVar4 = (bool)((byte)(uVar8 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
          uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
          cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
          uVar8 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
          uVar41 = uVar7 | uVar13 & 0xfffffeff | uVar8;
          uVar7 = uVar7 | uVar13 & 0xfffffefe;
          uVar13 = uVar7 | uVar8;
          uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x20) != 0);
          bVar3 = ((byte)(uVar13 >> 8) & 1) == ((byte)(uVar13 >> 9) & 1);
          bVar4 = (bool)((byte)(uVar13 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
          uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
          cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
          uVar13 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
          uVar42 = uVar7 | uVar8 & 0xfffffeff | uVar13;
          uVar7 = uVar7 | uVar8 & 0xfffffefe;
          uVar8 = uVar7 | uVar13;
          uVar11 = uVar10 * 2 | (uint)((uVar12 & 0x10) != 0);
          bVar3 = ((byte)(uVar8 >> 8) & 1) == ((byte)(uVar8 >> 9) & 1);
          bVar4 = (bool)((byte)(uVar8 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
          uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
          cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
          uVar8 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
          uVar43 = uVar7 | uVar13 & 0xfffffeff | uVar8;
          uVar7 = uVar7 | uVar13 & 0xfffffefe;
          uVar13 = uVar7 | uVar8;
          uVar11 = uVar10 * 2 | (uint)((uVar12 & 8) != 0);
          bVar3 = ((byte)(uVar13 >> 8) & 1) == ((byte)(uVar13 >> 9) & 1);
          bVar4 = (bool)((byte)(uVar13 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
          uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
          cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
          uVar13 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
          uVar44 = uVar7 | uVar8 & 0xfffffeff | uVar13;
          uVar7 = uVar7 | uVar8 & 0xfffffefe;
          uVar8 = uVar7 | uVar13;
          uVar11 = uVar10 * 2 | (uint)((uVar12 & 4) != 0);
          bVar3 = ((byte)(uVar8 >> 8) & 1) == ((byte)(uVar8 >> 9) & 1);
          bVar4 = (bool)((byte)(uVar8 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
          uVar10 = (uint)bVar3 * (uVar11 - param_2) + (uint)!bVar3 * (uVar11 + param_2);
          cVar2 = bVar3 * (uVar11 < uVar10) + !bVar3 * (uVar10 < uVar11);
          uVar8 = (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
          uVar11 = uVar7 | uVar13 & 0xfffffeff | uVar8;
          uVar7 = uVar7 | uVar13 & 0xfffffefe;
          uVar13 = uVar7 | uVar8;
          uVar12 = uVar10 * 2 | (uint)((uVar12 & 2) != 0);
          bVar3 = ((byte)(uVar13 >> 8) & 1) == ((byte)(uVar13 >> 9) & 1);
          bVar4 = (bool)((byte)(uVar13 >> 9) & 1) == ((uVar10 & 0x80000000) != 0);
          uVar13 = (uint)bVar3 * (uVar12 - param_2) + (uint)!bVar3 * (uVar12 + param_2);
          cVar2 = bVar3 * (uVar12 < uVar13) + !bVar3 * (uVar13 < uVar12);
          uVar13 = uVar7 | uVar8 & 0xfffffeff |
                   (uint)(byte)(bVar4 * cVar2 + (!bVar4 && cVar2 == '\0')) << 8;
          uVar5 = ((((((((((((((((((((((((((((((((uint)(((byte)((uVar5 | uVar14) >> 8) & 1) ==
                                                       ((byte)((uVar5 | uVar14) >> 9) & 1)) << 1 |
                                                (uint)(((byte)(uVar16 >> 8) & 1) ==
                                                      ((byte)(uVar16 >> 9) & 1))) << 1 |
                                               (uint)(((byte)(uVar17 >> 8) & 1) ==
                                                     ((byte)(uVar17 >> 9) & 1))) << 1 |
                                              (uint)(((byte)(uVar18 >> 8) & 1) ==
                                                    ((byte)(uVar18 >> 9) & 1))) << 1 |
                                             (uint)(((byte)(uVar19 >> 8) & 1) ==
                                                   ((byte)(uVar19 >> 9) & 1))) << 1 |
                                            (uint)(((byte)(uVar20 >> 8) & 1) ==
                                                  ((byte)(uVar20 >> 9) & 1))) << 1 |
                                           (uint)(((byte)(uVar21 >> 8) & 1) ==
                                                 ((byte)(uVar21 >> 9) & 1))) << 1 |
                                          (uint)(((byte)(uVar22 >> 8) & 1) ==
                                                ((byte)(uVar22 >> 9) & 1))) << 1 |
                                         (uint)(((byte)(uVar23 >> 8) & 1) ==
                                               ((byte)(uVar23 >> 9) & 1))) << 1 |
                                        (uint)(((byte)(uVar24 >> 8) & 1) ==
                                              ((byte)(uVar24 >> 9) & 1))) << 1 |
                                       (uint)(((byte)(uVar25 >> 8) & 1) == ((byte)(uVar25 >> 9) & 1)
                                             )) << 1 |
                                      (uint)(((byte)(uVar26 >> 8) & 1) == ((byte)(uVar26 >> 9) & 1))
                                      ) << 1 | (uint)(((byte)(uVar27 >> 8) & 1) ==
                                                     ((byte)(uVar27 >> 9) & 1))) << 1 |
                                    (uint)(((byte)(uVar28 >> 8) & 1) == ((byte)(uVar28 >> 9) & 1)))
                                    << 1 | (uint)(((byte)(uVar29 >> 8) & 1) ==
                                                 ((byte)(uVar29 >> 9) & 1))) << 1 |
                                  (uint)(((byte)(uVar30 >> 8) & 1) == ((byte)(uVar30 >> 9) & 1))) <<
                                  1 | (uint)(((byte)(uVar31 >> 8) & 1) == ((byte)(uVar31 >> 9) & 1))
                                 ) << 1 | (uint)(((byte)(uVar32 >> 8) & 1) ==
                                                ((byte)(uVar32 >> 9) & 1))) << 1 |
                               (uint)(((byte)(uVar33 >> 8) & 1) == ((byte)(uVar33 >> 9) & 1))) << 1
                              | (uint)(((byte)(uVar34 >> 8) & 1) == ((byte)(uVar34 >> 9) & 1))) << 1
                             | (uint)(((byte)(uVar35 >> 8) & 1) == ((byte)(uVar35 >> 9) & 1))) << 1
                            | (uint)(((byte)(uVar36 >> 8) & 1) == ((byte)(uVar36 >> 9) & 1))) << 1 |
                           (uint)(((byte)(uVar37 >> 8) & 1) == ((byte)(uVar37 >> 9) & 1))) << 1 |
                          (uint)(((byte)(uVar38 >> 8) & 1) == ((byte)(uVar38 >> 9) & 1))) << 1 |
                         (uint)(((byte)(uVar39 >> 8) & 1) == ((byte)(uVar39 >> 9) & 1))) << 1 |
                        (uint)(((byte)(uVar40 >> 8) & 1) == ((byte)(uVar40 >> 9) & 1))) << 1 |
                       (uint)(((byte)(uVar41 >> 8) & 1) == ((byte)(uVar41 >> 9) & 1))) << 1 |
                      (uint)(((byte)(uVar42 >> 8) & 1) == ((byte)(uVar42 >> 9) & 1))) << 1 |
                     (uint)(((byte)(uVar43 >> 8) & 1) == ((byte)(uVar43 >> 9) & 1))) << 1 |
                    (uint)(((byte)(uVar44 >> 8) & 1) == ((byte)(uVar44 >> 9) & 1))) << 1 |
                   (uint)(((byte)(uVar11 >> 8) & 1) == ((byte)(uVar11 >> 9) & 1))) << 1 |
                  (uint)(((byte)(uVar13 >> 8) & 1) == ((byte)(uVar13 >> 9) & 1))) +
                  (uint)(bVar1 != (int)uVar9 < 0);
        }
      }
      return CONCAT44(puVar6,uVar5);
    }
  }
  return CONCAT44(in_r1,uVar5);
}

