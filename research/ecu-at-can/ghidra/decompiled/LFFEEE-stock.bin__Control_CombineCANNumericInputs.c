/* Ghidra analysis output; verify against original SH instructions. */

/* Full execution throughA7432 with four independent numeric output oracles.
   A710=max(21Aword1/divisor,218byte6,-10000)+71C4;
   A70C=min(max(211numeric,21Aword0,-10000)/divisor,216limit)+71C4. Further histories/maps execute
   but are not independently modeled; physical role unproved. numeric-arbitration.txt. */

void Control_CombineCANNumericInputs(void)

{
  bool bVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined *puVar5;
  undefined *puVar6;
  undefined *puVar7;
  undefined *puVar8;
  undefined *puVar9;
  undefined *puVar10;
  undefined *puVar11;
  int iVar12;
  int iVar13;
  char cVar14;
  undefined1 uVar15;
  char cVar16;
  float fVar17;
  undefined4 uVar18;
  float fVar19;
  float fVar20;
  undefined4 uVar21;
  undefined4 uVar22;
  float fVar23;
  float fVar24;
  float fVar25;
  float fVar26;
  float fVar27;
  char acStack_10030 [65532];
  float fStack_34;
  float local_30 [2];
  char local_28 [4];
  char local_24 [4];
  char local_20 [4];
  
  puVar3 = PTR_DAT_000a65c8;
  puVar2 = PTR_Lookup_FloatCurve_000a65c4;
  iVar12 = (int)DAT_000a65b4;
  *(undefined4 *)((int)local_30 + iVar12 + 4) = *(undefined4 *)PTR_DAT_000a65bc;
  fVar27 = *(float *)PTR_DAT_000a65c0;
  *(float *)((int)&fStack_34 + iVar12) = *(float *)PTR_DAT_000a65cc - *(float *)PTR_DAT_000a65c8;
  fVar17 = (float)(*(code *)PTR_Lookup_FloatCurve_000a65c4)(fVar27,DAT_000a65d0);
  puVar4 = PTR_FUN_000a65d4;
  *(float *)((int)local_30 + DAT_000a65b6 + iVar12) =
       *(float *)puVar3 + *(float *)((int)&fStack_34 + iVar12) * fVar17;
  uVar18 = (*(code *)PTR_FUN_000a65d4)(PTR_DAT_000a65d8);
  *(undefined4 *)((int)local_30 + iVar12) = uVar18;
  fVar19 = (float)(*(code *)puVar4)(PTR_Control_RawSecondPublished_000a65dc);
  uVar18 = (*(code *)puVar4)(PTR_Model_ScaledAuxiliaryOffset_000a65e0);
  *(undefined4 *)(&stack0xfffffff4 + iVar12) = uVar18;
  uVar18 = (*(code *)puVar4)(PTR_Model_ReferenceAuxiliaryOffset_000a65e4);
  *(undefined4 *)(&stack0xfffffff0 + iVar12) = uVar18;
  fVar24 = DAT_000a65e8;
  fVar20 = (float)(*(code *)puVar4)(PTR_DAT_000a65ec);
  puVar8 = PTR_DAT_000a6608;
  puVar6 = PTR_DAT_000a6600;
  puVar5 = PTR_DAT_000a65fc;
  fVar17 = *(float *)((int)local_30 + iVar12);
  if (*(float *)((int)local_30 + iVar12) <= fVar24) {
    fVar17 = fVar24;
  }
  *(float *)(&stack0x00000000 + iVar12) = fVar19 + DAT_000a65f8;
  iVar13 = (int)DAT_000a65b6;
  *(float *)PTR_DAT_000a65fc =
       ((((fVar20 * DAT_000a65f0) / DAT_000a65f4) / fVar17) * (fVar19 + DAT_000a65f8) -
       *(float *)(&stack0xfffffff4 + iVar12)) - *(float *)(&stack0xfffffff0 + iVar12);
  puVar7 = PTR_DAT_000a6604;
  fVar17 = *(float *)puVar5 - *(float *)((int)local_30 + iVar13 + iVar12);
  *(float *)puVar6 = fVar17;
  puVar6 = PTR_SpeedCandidate_ProtectedSelected_000a6610;
  puVar5 = PTR_DAT_000a660c;
  fVar17 = fVar17 + (*(float *)puVar7 - fVar17) * *(float *)puVar8;
  *(float *)(&stack0x00000040 + iVar12) = fVar17;
  *(float *)PTR_DAT_000a660c = fVar17 + *(float *)((int)local_30 + iVar12 + 4);
  uVar18 = (*(code *)puVar4)(puVar6);
  *(undefined4 *)(&stack0xffffffe8 + iVar12) = uVar18;
  if (puVar3[0x2c] == '\0') {
    bVar1 = *(float *)PTR_DAT_000a6614 < *(float *)(&stack0xffffffe8 + iVar12);
  }
  else {
    bVar1 = *(float *)PTR_DAT_000a6614 - *(float *)PTR_DAT_000a6618 <
            *(float *)(&stack0xffffffe8 + iVar12);
  }
  *(bool *)((int)local_30 + DAT_000a65b8 + iVar12) = bVar1;
  cVar14 = (*(code *)PTR_FUN_000a6620)(PTR_DAT_000a661c);
  puVar6 = PTR_DAT_000a6720;
  if (((*(char *)((int)local_30 + DAT_000a65b8 + iVar12) == '\0') ||
      (fVar27 <= *(float *)PTR_DAT_000a6624)) || (cVar14 != '\0')) {
    uVar15 = 0;
  }
  else {
    uVar15 = 1;
  }
  (&stack0x00000008)[iVar12] = uVar15;
  if ((*(float *)PTR_DAT_000a6718 <= *(float *)(&stack0xffffffe8 + iVar12)) || (cVar14 == '\0')) {
    cVar14 = '\0';
  }
  else {
    cVar14 = '\x01';
  }
  *PTR_DAT_000a671c = cVar14;
  uVar18 = *(undefined4 *)puVar6;
  if (cVar14 == '\0') {
    uVar22 = (*(code *)puVar2)(uVar18,DAT_000a6728);
    *(undefined4 *)(&stack0x0000003c + iVar12) = uVar22;
  }
  else {
    *(undefined4 *)(&stack0x0000003c + iVar12) = *(undefined4 *)PTR_DAT_000a6724;
  }
  puVar6 = PTR_DAT_000a6740;
  *(undefined4 *)((int)local_30 + DAT_000a670e + iVar12) = *(undefined4 *)(puVar3 + 4);
  *(undefined4 *)(&stack0x00000018 + iVar12) = *(undefined4 *)(puVar3 + 8);
  *(undefined4 *)((int)local_30 + DAT_000a6710 + iVar12) = *(undefined4 *)PTR_DAT_000a672c;
  fVar17 = *(float *)PTR_DAT_000a6730;
  if (*PTR_DAT_000a671c == '\0') {
    uVar22 = *(undefined4 *)PTR_DAT_000a6738;
  }
  else {
    uVar22 = *(undefined4 *)PTR_DAT_000a6734;
  }
  *(undefined4 *)(&stack0x00000004 + iVar12) = uVar22;
  if (puVar3[0x2d] == '\0') {
    fVar19 = *(float *)(&stack0x00000004 + iVar12);
  }
  else {
    fVar19 = *(float *)(&stack0x00000004 + iVar12) - *(float *)PTR_DAT_000a673c;
  }
  *(bool *)((int)local_30 + DAT_000a6712 + iVar12) = fVar19 < fVar27;
  fVar19 = 0.0;
  if (*(char *)((int)local_30 + DAT_000a6712 + iVar12) == '\0') {
    fVar17 = 0.0;
  }
  else {
    fVar17 = *(float *)PTR_DAT_000a6740 + fVar17;
  }
  fVar20 = DAT_000a6744;
  if (fVar17 <= DAT_000a6744) {
    fVar20 = fVar17;
  }
  *(float *)((int)local_30 + DAT_000a6714 + iVar12) = fVar20;
  *(undefined4 *)((int)local_30 + DAT_000a6716 + iVar12) = *(undefined4 *)PTR_DAT_000a6748;
  fVar17 = (float)(*(code *)puVar2)(uVar18,DAT_000a674c);
  uVar22 = DAT_000a6858;
  if (fVar17 <= *(float *)((int)local_30 + DAT_000a6714 + iVar12)) {
    fVar17 = *(float *)((int)local_30 + DAT_000a6836 + iVar12) - *(float *)PTR_DAT_000a6844;
    if (fVar17 <= 0.0) {
      fVar17 = 0.0;
    }
    *(float *)(&stack0x00000014 + iVar12) = fVar17;
  }
  else {
    *(undefined4 *)(&stack0x00000014 + iVar12) = *(undefined4 *)PTR_DAT_000a6750;
  }
  if (DAT_000a6848 <= *(float *)(&stack0x00000014 + iVar12)) {
    *(float *)((int)local_30 + DAT_000a683a + iVar12) = fVar19;
  }
  else {
    fVar20 = *(float *)puVar6 + *(float *)((int)local_30 + DAT_000a6838 + iVar12);
    fVar17 = DAT_000a684c;
    if (fVar20 <= DAT_000a684c) {
      fVar17 = fVar20;
    }
    *(float *)((int)local_30 + DAT_000a683a + iVar12) = fVar17;
  }
  *PTR_DAT_000a6854 = *(float *)PTR_DAT_000a6850 < *(float *)((int)local_30 + DAT_000a683a + iVar12)
  ;
  fVar17 = (float)(*(code *)puVar2)(uVar18,uVar22);
  if ((*(float *)PTR_DAT_000a685c + fVar17 <= *(float *)(&stack0x00000018 + iVar12)) ||
     (*PTR_DAT_000a6854 == '\0')) {
    *(float *)((int)local_30 + DAT_000a683c + iVar12) = fVar19;
  }
  else {
    *(float *)((int)local_30 + DAT_000a683c + iVar12) =
         *(float *)puVar6 + *(float *)(&stack0x00000018 + iVar12);
  }
  bVar1 = *(float *)PTR_DAT_000a685c < *(float *)((int)local_30 + DAT_000a683c + iVar12);
  (&stack0x0000002c)[iVar12] = bVar1;
  if (bVar1) {
    fVar17 = (float)(*(code *)puVar2)(uVar18,DAT_000a6860);
    fVar17 = *(float *)((int)local_30 + DAT_000a683e + iVar12) + fVar17;
    if (*(float *)PTR_DAT_000a6864 < fVar17) {
      fVar17 = *(float *)PTR_DAT_000a6864;
    }
    *(float *)((int)local_30 + DAT_000a6840 + iVar12) = fVar17;
  }
  else {
    *(float *)((int)local_30 + DAT_000a6840 + iVar12) = fVar19;
  }
  puVar8 = PTR_DAT_000a6868;
  if (*PTR_DAT_000a6854 == '\0') {
    *(float *)PTR_DAT_000a6868 = fVar19;
  }
  else {
    *(undefined4 *)PTR_DAT_000a6868 = *(undefined4 *)((int)local_30 + DAT_000a6840 + iVar12);
  }
  puVar7 = PTR_DAT_000a6970;
  fVar17 = *(float *)puVar8 + *(float *)(&stack0x00000004 + iVar12) +
           *(float *)(&stack0x00000014 + iVar12);
  *(float *)PTR_DAT_000a696c = fVar17;
  puVar9 = PTR_DAT_000a697c;
  puVar8 = PTR_DAT_000a6978;
  *(float *)(&stack0xffffffec + iVar12) = fVar27 - fVar17;
  if (puVar3[0x2e] == '\0') {
    bVar1 = *(float *)(&stack0x0000003c + iVar12) < *(float *)(&stack0xffffffec + iVar12);
  }
  else {
    bVar1 = *(float *)(&stack0x0000003c + iVar12) - *(float *)PTR_DAT_000a6974 <
            *(float *)(&stack0xffffffec + iVar12);
  }
  *puVar7 = bVar1;
  puVar10 = PTR_DAT_000a6984;
  (&stack0x0000004c)[iVar12] = *puVar8;
  fVar17 = fVar19;
  if (*puVar7 != '\0') {
    fVar17 = *(float *)puVar6 + *(float *)puVar9;
  }
  fVar20 = DAT_000a6980;
  if (fVar17 <= DAT_000a6980) {
    fVar20 = fVar17;
  }
  *(float *)(&stack0x00000048 + iVar12) = fVar20;
  uVar15 = puVar3[0x30];
  if ((*(float *)PTR_DAT_000a6988 == 0.0) ||
     ((puVar3[0x2f] != '\0' && ((&stack0x0000004c)[iVar12] == '\0')))) {
    *PTR_DAT_000a6984 = 0;
  }
  else {
    if ((*(float *)PTR_DAT_000a698c <= *(float *)(&stack0x00000048 + iVar12)) &&
       (*(float *)PTR_DAT_000a6990 == 0.0)) {
      uVar15 = 1;
    }
    *PTR_DAT_000a6984 = uVar15;
  }
  *(undefined4 *)((int)local_30 + DAT_000a6966 + iVar12) = *(undefined4 *)(puVar3 + 0xc);
  uVar22 = (*(code *)puVar4)(PTR_CAN218_Byte6Request_000a6994);
  *(undefined4 *)((int)local_30 + DAT_000a6968 + iVar12) = uVar22;
  cVar14 = (*(code *)PTR_FUN_000a699c)(PTR_CAN211_ConversionBypass_000a6998);
  local_28[iVar12] = cVar14;
  fVar17 = (float)(*(code *)puVar4)(PTR_CAN211_ConversionFactor_000a69a0);
  *(float *)(&stack0xffffffe4 + iVar12) = fVar17;
  if (local_28[iVar12] == '\0') {
    fVar20 = fVar24;
    if (fVar24 <= fVar17) {
      fVar20 = *(float *)(&stack0xffffffe4 + iVar12);
    }
  }
  else {
    fVar20 = 1.0;
  }
  *(float *)(&stack0x0000000c + iVar12) = fVar20;
  fVar20 = (float)(*(code *)puVar4)(PTR_CAN21A_GatedWord1Value_000a6ab4);
  fVar23 = *(float *)(&stack0x0000000c + iVar12);
  *(float *)(&stack0x0000000c + iVar12) = fVar20 / fVar23;
  fVar17 = *(float *)((int)local_30 + DAT_000a6aaa + iVar12);
  if (fVar17 < fVar20 / fVar23) {
    fVar17 = *(float *)(&stack0x0000000c + iVar12);
  }
  if (fVar17 < *(float *)PTR_DAT_000a6ab8) {
    fVar17 = *(float *)PTR_DAT_000a6ab8;
  }
  *(float *)((int)local_30 + DAT_000a6aac + iVar12) = fVar17;
  fVar17 = (float)(*(code *)puVar4)(PTR_CAN215_SharedModelOffset_000a6abc);
  puVar8 = PTR_CANModel_MaxCombinedValue_000a6ac0;
  *(float *)(&stack0x0000001c + iVar12) = fVar17;
  *(float *)PTR_CANModel_MaxCombinedValue_000a6ac0 =
       *(float *)((int)local_30 + DAT_000a6aac + iVar12) + fVar17;
  puVar9 = PTR_CANModel_ConvertedMaxValue_000a6acc;
  fVar17 = *(float *)((int)local_30 + iVar12);
  if (*(float *)((int)local_30 + iVar12) <= fVar24) {
    fVar17 = fVar24;
  }
  *(float *)PTR_CANModel_ConvertedMaxValue_000a6acc =
       ((((*(float *)puVar8 * DAT_000a6ac4) / DAT_000a6ac8) / fVar17) *
        *(float *)(&stack0x00000000 + iVar12) - *(float *)(&stack0xfffffff4 + iVar12)) -
       *(float *)(&stack0xfffffff0 + iVar12);
  if (*(float *)puVar9 <= *(float *)puVar5) {
    *(float *)((int)local_30 + DAT_000a6ab0 + iVar12) = fVar19;
  }
  else {
    *(float *)((int)local_30 + DAT_000a6ab0 + iVar12) =
         *(float *)((int)local_30 + DAT_000a6aae + iVar12) + DAT_000a6ad0;
  }
  local_20[iVar12] = *(float *)((int)local_30 + DAT_000a6ab0 + iVar12) < *(float *)PTR_DAT_000a6ad4;
  fVar17 = (float)(*(code *)puVar2)(fVar27,DAT_000a6ad8);
  puVar8 = PTR_CAN211_NumericBound_000a6ae4;
  *(float *)(&stack0x00000034 + iVar12) = fVar17;
  if ((local_20[iVar12] == '\0') || (fVar17 <= *(float *)PTR_DAT_000a6adc)) {
    uVar15 = 1;
  }
  else {
    uVar15 = 0;
  }
  *PTR_DAT_000a6ae0 = uVar15;
  fVar17 = (float)(*(code *)puVar4)(puVar8);
  puVar8 = PTR_CANModel_ATBoundedValue_000a6cf0;
  if (fVar17 <= *(float *)PTR_DAT_000a6ae8) {
    fVar17 = *(float *)PTR_DAT_000a6ae8;
  }
  fVar20 = *(float *)PTR_CAN21A_Word0Value_000a6aec;
  if (local_28[iVar12] == '\0') {
    fVar23 = fVar24;
    if (fVar24 <= *(float *)(&stack0xffffffe4 + iVar12)) {
      fVar23 = *(float *)(&stack0xffffffe4 + iVar12);
    }
  }
  else {
    fVar23 = 1.0;
  }
  if (fVar20 <= fVar17) {
    fVar20 = fVar17;
  }
  fVar20 = fVar20 / fVar23;
  if (*(float *)PTR_CAN216_Word1Limit_000a6cec <= fVar20) {
    fVar20 = *(float *)PTR_CAN216_Word1Limit_000a6cec;
  }
  *(float *)PTR_CANModel_ATBoundedValue_000a6cf0 = fVar20 + *(float *)(&stack0x0000001c + iVar12);
  puVar9 = PTR_CANModel_ConvertedATBoundedValue_000a6cfc;
  fVar17 = *(float *)((int)local_30 + iVar12);
  if (*(float *)((int)local_30 + iVar12) <= fVar24) {
    fVar17 = fVar24;
  }
  *(float *)PTR_CANModel_ConvertedATBoundedValue_000a6cfc =
       ((((*(float *)puVar8 * DAT_000a6cf4) / DAT_000a6cf8) / fVar17) *
        *(float *)(&stack0x00000000 + iVar12) - *(float *)(&stack0xfffffff4 + iVar12)) -
       *(float *)(&stack0xfffffff0 + iVar12);
  puVar8 = PTR_CANModel_LimitedATBoundedValue_000a6d00;
  fVar17 = *(float *)puVar9;
  if (*(float *)puVar5 < fVar17) {
    fVar17 = *(float *)puVar5;
  }
  *(float *)PTR_CANModel_LimitedATBoundedValue_000a6d00 = fVar17;
  *(float *)((int)&fStack_34 + iVar12) = *(float *)PTR_DAT_000a6d04 - *(float *)puVar8;
  fVar17 = (float)(*(code *)puVar2)(fVar27,DAT_000a6d08);
  puVar9 = PTR_Control_LimitedInverseValue_000a6d20;
  puVar8 = PTR_CANModel_ConvertedATBoundedValue_000a6cfc;
  *(float *)(&stack0xfffffffc + iVar12) =
       *(float *)PTR_CANModel_LimitedATBoundedValue_000a6d00 +
       *(float *)((int)&fStack_34 + iVar12) * fVar17;
  fVar17 = *(float *)PTR_CANModel_ConvertedATBoundedValue_000a6cfc;
  if (puVar3[0x31] != '\0') {
    fVar17 = fVar17 + *(float *)PTR_DAT_000a6d0c;
  }
  local_28[iVar12] = *(float *)puVar5 < fVar17;
  if (((local_28[iVar12] == '\0') && (*PTR_DAT_000a6d10 == '\0')) && (*PTR_DAT_000a6d14 == '\0')) {
    bVar1 = false;
  }
  else {
    bVar1 = true;
  }
  fVar17 = *(float *)((int)local_30 + iVar12);
  if (*(float *)((int)local_30 + iVar12) <= fVar24) {
    fVar17 = fVar24;
  }
  fVar17 = ((((*(float *)PTR_DAT_000a6d1c * DAT_000a6cf4) / DAT_000a6cf8) / fVar17) *
            *(float *)(&stack0x00000000 + iVar12) - *(float *)(&stack0xfffffff4 + iVar12)) -
           *(float *)(&stack0xfffffff0 + iVar12);
  *(float *)PTR_DAT_000a6d18 = fVar17;
  puVar11 = PTR_DAT_000a6d24;
  fVar24 = *(float *)puVar8 - *(float *)(&stack0xfffffffc + iVar12);
  fVar17 = fVar17 - *(float *)(&stack0xfffffffc + iVar12);
  if (fVar24 < 0.0) {
    fVar24 = -fVar24;
  }
  if ((*(float *)PTR_DAT_000a6d28 <= fVar24) || (bVar1)) {
    *(float *)PTR_DAT_000a6d24 = fVar19;
  }
  else {
    fVar24 = fVar19;
    if ((((DAT_000a6d2c < *(float *)puVar9) || (fVar17 <= 0.0)) &&
        ((*(float *)puVar9 + *(float *)PTR_DAT_000a6d30 < DAT_000a6d34 || (0.0 <= fVar17)))) &&
       (*PTR_DAT_000a6d38 == '\0')) {
      fVar24 = fVar17;
    }
    *(float *)PTR_DAT_000a6d24 = *(float *)(puVar3 + 0x10) + *(float *)PTR_DAT_000a6d3c * fVar24;
  }
  puVar9 = PTR_DAT_000a6d50;
  puVar8 = PTR_DAT_000a6d48;
  fVar24 = DAT_000a6d40;
  if (*(float *)puVar11 < DAT_000a6d40) {
    fVar24 = *(float *)puVar11;
  }
  fVar20 = DAT_000a6d44;
  if (DAT_000a6d44 <= fVar24) {
    fVar20 = fVar24;
  }
  *(float *)(&stack0x00000038 + iVar12) = fVar20;
  fVar24 = DAT_000a6d4c;
  if (local_28[iVar12] == '\0') {
    if (bVar1) {
      *(float *)PTR_DAT_000a6d50 = fVar19;
    }
    else {
      *(float *)PTR_DAT_000a6d50 = fVar17;
    }
    puVar11 = PTR_DAT_000a6d54;
    *(float *)PTR_DAT_000a6d54 =
         *(float *)(&stack0x00000038 + iVar12) + *(float *)puVar9 * *(float *)PTR_DAT_000a6d58;
    fVar24 = *(float *)puVar11 + *(float *)PTR_CANModel_LimitedATBoundedValue_000a6d00;
  }
  *(float *)puVar8 = fVar24;
  puVar9 = PTR_DAT_000a6d5c;
  if (local_20[iVar12] == '\0') {
    fVar17 = *(float *)PTR_DAT_000a6e84;
  }
  else {
    fVar17 = *(float *)(&stack0x00000034 + iVar12);
  }
  *(float *)PTR_DAT_000a6d5c = fVar17;
  fVar24 = *(float *)PTR_CANModel_ConvertedMaxValue_000a6e88;
  if (fVar17 < fVar24) {
    fVar24 = *(float *)puVar9;
  }
  fVar20 = *(float *)((int)local_30 + iVar12 + 4);
  fVar17 = (fVar24 - *(float *)puVar5) + fVar20;
  if (*(float *)puVar9 < fVar17) {
    fVar17 = *(float *)puVar9;
  }
  fVar17 = fVar17 - fVar20;
  if (fVar17 < 0.0) {
    fVar17 = 0.0;
  }
  *(float *)PTR_DAT_000a6e8c = fVar17;
  puVar5 = PTR_DAT_000a6e90;
  *(float *)((int)local_30 + iVar12 + 4) = fVar17 + fVar20;
  if (*(float *)puVar8 < fVar17 + fVar20) {
    uVar22 = *(undefined4 *)puVar8;
  }
  else {
    uVar22 = *(undefined4 *)((int)local_30 + iVar12 + 4);
  }
  *(undefined4 *)PTR_DAT_000a6e90 = uVar22;
  local_24[iVar12] = *PTR_DAT_000a6e94;
  fVar20 = *(float *)PTR_DAT_000a6e98;
  fVar24 = *(float *)(&stack0xffffffe8 + iVar12);
  fVar17 = *(float *)PTR_DAT_000a6e9c;
  *(float *)PTR_DAT_000a6ea0 = fVar17 - fVar24;
  if (local_24[iVar12] == '\0') {
    if ((&stack0x00000008)[iVar12] == '\0') {
      uVar22 = (*(code *)puVar2)(*(undefined4 *)puVar5,DAT_000a6eb0);
      *(undefined4 *)PTR_DAT_000a6eac = uVar22;
    }
    else {
      *(float *)PTR_DAT_000a6eac = fVar20 + (fVar17 - fVar24) * *(float *)PTR_DAT_000a6ea8;
    }
    *(undefined4 *)(&stack0x00000010 + iVar12) = *(undefined4 *)PTR_DAT_000a6eac;
  }
  else {
    *(undefined4 *)(&stack0x00000010 + iVar12) = *(undefined4 *)PTR_DAT_000a6ea4;
  }
  puVar8 = PTR_DAT_000a6ec8;
  fVar24 = *(float *)puVar5;
  fVar17 = *(float *)PTR_DAT_000a6eb4;
  if (fVar24 < *(float *)PTR_DAT_000a6eb4) {
    fVar17 = fVar24;
  }
  if (*(float *)(&stack0x00000010 + iVar12) < fVar17) {
    fVar17 = *(float *)(&stack0x00000010 + iVar12);
  }
  fVar20 = *(float *)PTR_DAT_000a6eb8;
  if (fVar17 < *(float *)PTR_DAT_000a6ebc) {
    fVar17 = *(float *)PTR_DAT_000a6ebc;
  }
  if (fVar17 < fVar20) {
    fVar17 = fVar20;
  }
  *(float *)(&stack0x00000030 + iVar12) = fVar17;
  if ((&stack0x00000008)[iVar12] == '\0') {
    *(float *)PTR_DAT_000a6f9c = fVar24;
  }
  else {
    fVar24 = *(float *)PTR_DAT_000a6ec4;
    fVar17 = *(float *)PTR_DAT_000a6ea0;
    *(float *)PTR_DAT_000a6ec0 = fVar17 * fVar24;
    fVar17 = fVar17 * fVar24 + *(float *)(&stack0x00000030 + iVar12);
    *(float *)puVar8 = fVar17;
    if (*(float *)puVar5 < fVar17) {
      fVar17 = *(float *)puVar5;
    }
    else {
      fVar17 = *(float *)puVar8;
    }
    fVar24 = fVar20;
    if (fVar20 <= fVar17) {
      fVar24 = fVar17;
    }
    *(float *)PTR_DAT_000a6ecc = fVar24;
  }
  if ((&stack0x0000002c)[iVar12] == '\0') {
    uVar22 = (*(code *)puVar2)(uVar18,DAT_000a6fa0);
    *(undefined4 *)((int)local_30 + DAT_000a6f98 + iVar12) = uVar22;
  }
  else {
    *(undefined4 *)((int)local_30 + DAT_000a6f98 + iVar12) =
         *(undefined4 *)((int)local_30 + DAT_000a6f96 + iVar12);
  }
  if (*PTR_DAT_000a6fa4 == '\0') {
    fVar17 = (float)(*(code *)puVar2)(uVar18,DAT_000a6fac);
    if (0.0 <= fVar17) {
      fVar17 = 0.0;
    }
  }
  else {
    fVar17 = *(float *)PTR_DAT_000a6fa8;
  }
  if (*PTR_DAT_000a6fb0 == '\0') {
    bVar1 = fVar17 < *(float *)(&stack0xffffffec + iVar12);
  }
  else {
    bVar1 = fVar17 - *(float *)PTR_DAT_000a6fb4 < *(float *)(&stack0xffffffec + iVar12);
  }
  local_20[iVar12] = bVar1;
  fVar17 = fVar19;
  if (*puVar7 != '\0') {
    fVar17 = *(float *)puVar6 + *(float *)PTR_DAT_000a6fb8;
  }
  fVar24 = DAT_000a6fbc;
  if (fVar17 <= DAT_000a6fbc) {
    fVar24 = fVar17;
  }
  *(float *)(&stack0xfffffff8 + iVar12) = fVar24;
  fVar17 = (float)(*(code *)puVar2)(uVar18,DAT_000a6fc0);
  puVar6 = PTR_DAT_000a6fc4;
  *PTR_DAT_000a6fc4 = fVar17 < *(float *)(&stack0xfffffff8 + iVar12);
  puVar8 = PTR_DAT_000a70cc;
  if (((local_20[iVar12] == '\0') && (*puVar6 == '\0')) || (*PTR_DAT_000a6fc8 == '\0')) {
    uVar15 = 0;
  }
  else {
    uVar15 = 1;
  }
  *PTR_DAT_000a70c8 = uVar15;
  fVar17 = *(float *)puVar8;
  *(float *)PTR_DAT_000a70d0 = fVar27 - fVar17;
  fVar24 = -((fVar27 - fVar17) * 1.0);
  *(float *)PTR_DAT_000a70d8 = (-*(float *)(puVar3 + 0x14) + fVar24) / DAT_000a70d4;
  fVar17 = (float)(*(code *)puVar2)(uVar18,DAT_000a70dc);
  puVar6 = PTR_Lookup_FloatMap2D_000a70e4;
  *(float *)PTR_DAT_000a70e0 = fVar17 * *(float *)PTR_DAT_000a70d8;
  if (*PTR_DAT_000a70e8 == '\0') {
    uVar22 = (*(code *)puVar6)(*(undefined4 *)PTR_DAT_000a70d0,uVar18,DAT_000a70f0);
  }
  else {
    uVar22 = (*(code *)puVar2)(DAT_000a70ec);
  }
  puVar8 = PTR_DAT_000a70f4;
  *(undefined4 *)PTR_DAT_000a70f4 = uVar22;
  puVar11 = PTR_DAT_000a7100;
  puVar9 = PTR_DAT_000a70fc;
  iVar13 = (int)DAT_000a70c6;
  *(float *)PTR_DAT_000a70f8 = *(float *)puVar8 * fVar24;
  *(undefined4 *)((int)local_30 + iVar13 + iVar12) = *(undefined4 *)puVar9;
  *puVar11 = puVar3[0x33];
  if (*PTR_DAT_000a70c8 == '\0') {
    uVar22 = (*(code *)puVar2)(uVar18,DAT_000a7118);
    *(undefined4 *)PTR_DAT_000a7114 = uVar22;
  }
  else {
    if (*puVar11 == '\0') {
      if (local_24[iVar12] == '\0') {
        fVar17 = (float)(*(code *)puVar2)(fVar24,DAT_000a710c);
        *(float *)((int)&fStack_34 + iVar12) = fVar24 * fVar17;
        fVar17 = (float)(*(code *)puVar2)(uVar18,DAT_000a7110);
        fVar17 = *(float *)((int)&fStack_34 + iVar12) * fVar17;
      }
      else {
        fVar17 = (float)(*(code *)puVar2)(uVar18,DAT_000a7108);
      }
      *(float *)PTR_DAT_000a7104 = fVar17;
    }
    else {
      *(float *)PTR_DAT_000a7104 = fVar19;
    }
    *(float *)PTR_DAT_000a7114 =
         *(float *)PTR_DAT_000a7104 + *(float *)((int)local_30 + DAT_000a70c6 + iVar12);
  }
  fVar17 = *(float *)PTR_DAT_000a7114;
  if (*(float *)PTR_DAT_000a711c <= fVar17) {
    fVar17 = *(float *)PTR_DAT_000a711c;
  }
  if (fVar17 < *(float *)PTR_DAT_000a7120) {
    fVar17 = *(float *)PTR_DAT_000a7120;
  }
  *(float *)(&stack0x00000028 + iVar12) = fVar17;
  *(float *)PTR_DAT_000a72ac = *(float *)PTR_DAT_000a72a8 + *(float *)PTR_DAT_000a72a4 + fVar17;
  if (*puVar7 == '\0') {
    uVar22 = *(undefined4 *)puVar5;
  }
  else {
    uVar22 = *(undefined4 *)PTR_DAT_000a72ac;
  }
  *(undefined4 *)(&stack0x00000044 + iVar12) = uVar22;
  uVar22 = (*(code *)puVar4)(PTR_DAT_000a72b0);
  puVar2 = PTR_DAT_000a72bc;
  *(undefined4 *)(&stack0x00000024 + iVar12) = *(undefined4 *)PTR_DAT_000a72b4;
  *(undefined4 *)(&stack0x00000020 + iVar12) = *(undefined4 *)PTR_DAT_000a72b8;
  uVar21 = (*(code *)puVar6)(uVar22,*(undefined4 *)PTR_DAT_000a72bc,DAT_000a72c0);
  *(undefined4 *)((int)&fStack_34 + iVar12) = uVar21;
  fVar17 = (float)(*(code *)puVar6)(uVar22,*(undefined4 *)puVar2,DAT_000a72c4);
  *(float *)((int)&fStack_34 + iVar12) =
       *(float *)(&stack0x00000024 + iVar12) * fVar17 +
       *(float *)(&stack0x00000044 + iVar12) * *(float *)((int)&fStack_34 + iVar12);
  fVar17 = (float)(*(code *)puVar6)(uVar22,*(undefined4 *)puVar2,DAT_000a72c8);
  *(float *)((int)&fStack_34 + iVar12) =
       *(float *)((int)&fStack_34 + iVar12) + *(float *)(puVar3 + 0x18) * fVar17;
  fVar17 = (float)(*(code *)puVar6)(uVar22,*(undefined4 *)puVar2,DAT_000a72cc);
  *(float *)((int)&fStack_34 + iVar12) =
       *(float *)((int)&fStack_34 + iVar12) - fVar17 * *(float *)(&stack0x00000020 + iVar12);
  fVar17 = (float)(*(code *)puVar6)(uVar22,*(undefined4 *)puVar2,DAT_000a72d0);
  fVar19 = *(float *)((int)&fStack_34 + iVar12) - fVar17 * *(float *)(puVar3 + 0x1c);
  fVar17 = (float)(*(code *)puVar6)(*(undefined4 *)(&stack0xfffffff8 + iVar12),uVar18,DAT_000a72d4);
  puVar2 = PTR_DAT_000a72dc;
  *(float *)PTR_DAT_000a72d8 = fVar19 * fVar17;
  fVar17 = *(float *)PTR_DAT_000a72ac - fVar19 * fVar17;
  *(float *)puVar2 = fVar17;
  puVar6 = PTR_DAT_000a72ec;
  puVar4 = PTR_DAT_000a72e8;
  if (*(float *)puVar5 < fVar17) {
    fVar17 = *(float *)puVar5;
  }
  else {
    fVar17 = *(float *)puVar2;
  }
  if (fVar17 < fVar20) {
    fVar17 = fVar20;
  }
  if (fVar17 < *(float *)PTR_DAT_000a72e0) {
    fVar17 = *(float *)PTR_DAT_000a72e0;
  }
  *(float *)PTR_DAT_000a72e4 = fVar17;
  puVar8 = PTR_DAT_000a72f4;
  fVar27 = *(float *)puVar2;
  uVar18 = *(undefined4 *)(puVar3 + 0x20);
  uVar22 = *(undefined4 *)(puVar3 + 0x24);
  local_24[iVar12] = puVar3[0x34];
  fVar23 = *(float *)puVar4 + *(float *)puVar6;
  fVar20 = DAT_000a72f0;
  if (fVar23 <= DAT_000a72f0) {
    fVar20 = fVar23;
  }
  if (*puVar7 == '\0') {
    *(undefined4 *)PTR_DAT_000a72f4 = *(undefined4 *)puVar5;
  }
  else {
    *(float *)PTR_DAT_000a72f4 = fVar17;
  }
  puVar6 = PTR_DAT_000a7450;
  puVar2 = PTR_Control_InverseTargetInput_000a744c;
  cVar14 = *puVar10;
  fVar23 = *(float *)puVar8;
  if ((cVar14 == '\0') || (fVar26 = fVar23, local_24[iVar12] != '\0')) {
    fVar26 = *(float *)(puVar3 + 0x28);
  }
  local_24[iVar12] = puVar3[0x35];
  cVar16 = puVar3[0x36];
  if (fVar20 < fVar23) {
    if ((local_24[iVar12] != '\0') && (cVar14 == '\0')) {
      cVar16 = '\x01';
    }
  }
  else {
    cVar16 = '\0';
  }
  fVar25 = fVar26;
  if ((cVar14 == '\0') && (fVar25 = fVar23, cVar16 != '\0')) {
    fVar25 = fVar20;
  }
  fVar20 = *(float *)PTR_DAT_000a7448;
  if (*(float *)puVar5 < *(float *)PTR_DAT_000a7448) {
    fVar20 = *(float *)puVar5;
  }
  if (fVar25 < fVar20) {
    fVar20 = fVar25;
  }
  *(float *)PTR_Control_InverseTargetInput_000a744c = fVar20;
  *(undefined4 *)puVar6 = *(undefined4 *)(&stack0x00000040 + iVar12);
  *(undefined4 *)PTR_DAT_000a7454 = *(undefined4 *)((int)local_30 + DAT_000a7434 + iVar12);
  *(undefined4 *)puVar3 = *(undefined4 *)puVar2;
  puVar2 = PTR_DAT_000a7458;
  puVar3[0x2c] = *(undefined1 *)((int)local_30 + DAT_000a7436 + iVar12);
  puVar5 = PTR_DAT_000a745c;
  *(undefined4 *)(puVar3 + 4) = *(undefined4 *)((int)local_30 + DAT_000a7438 + iVar12);
  *(undefined4 *)(puVar3 + 8) = *(undefined4 *)((int)local_30 + DAT_000a743a + iVar12);
  *(undefined4 *)puVar2 = *(undefined4 *)((int)local_30 + DAT_000a743c + iVar12);
  *(undefined4 *)puVar5 = *(undefined4 *)((int)local_30 + DAT_000a743e + iVar12);
  puVar2 = PTR_DAT_000a7460;
  puVar3[0x2d] = *(undefined1 *)((int)local_30 + DAT_000a7440 + iVar12);
  *(undefined4 *)puVar2 = *(undefined4 *)(&stack0x00000014 + iVar12);
  puVar3[0x2e] = *puVar7;
  puVar5 = PTR_DAT_000a7468;
  puVar2 = PTR_DAT_000a7464;
  puVar3[0x2f] = (&stack0x0000004c)[iVar12];
  *(undefined4 *)puVar2 = *(undefined4 *)(&stack0x00000048 + iVar12);
  puVar3[0x30] = *puVar10;
  *(undefined4 *)(puVar3 + 0xc) = *(undefined4 *)((int)local_30 + DAT_000a7442 + iVar12);
  *(undefined4 *)puVar5 = *(undefined4 *)(&stack0xfffffffc + iVar12);
  puVar3[0x31] = local_28[iVar12];
  *PTR_DAT_000a746c = (&stack0x00000008)[iVar12];
  puVar5 = PTR_DAT_000a7474;
  puVar3[0x32] = *puVar7;
  puVar2 = PTR_DAT_000a7470;
  *(undefined4 *)(puVar3 + 0x10) = *(undefined4 *)(&stack0x00000038 + iVar12);
  *(undefined4 *)puVar2 = *(undefined4 *)(&stack0x00000010 + iVar12);
  puVar2 = PTR_DAT_000a747c;
  *(undefined4 *)puVar5 = *(undefined4 *)(&stack0x00000030 + iVar12);
  *PTR_DAT_000a7478 = local_20[iVar12];
  *(undefined4 *)puVar2 = *(undefined4 *)(&stack0xfffffff8 + iVar12);
  *(undefined4 *)(puVar3 + 0x14) = uVar22;
  puVar2 = PTR_DAT_000a7484;
  *(undefined4 *)PTR_DAT_000a7480 = *(undefined4 *)(&stack0x00000028 + iVar12);
  puVar5 = PTR_DAT_000a7488;
  puVar3[0x33] = -((fVar27 == fVar17) + -1);
  *(undefined4 *)puVar2 = *(undefined4 *)(&stack0x00000044 + iVar12);
  *(undefined4 *)(puVar3 + 0x18) = *(undefined4 *)(&stack0x00000024 + iVar12);
  *(float *)puVar5 = fVar19;
  *(undefined4 *)(puVar3 + 0x1c) = *(undefined4 *)(&stack0x00000020 + iVar12);
  *(float *)(puVar3 + 0x20) = fVar24;
  *(undefined4 *)(puVar3 + 0x24) = uVar18;
  puVar3[0x34] = *puVar10;
  *(float *)puVar4 = fVar25;
  *(float *)(puVar3 + 0x28) = fVar26;
  puVar3[0x35] = *puVar10;
  puVar3[0x36] = cVar16;
  return;
}

