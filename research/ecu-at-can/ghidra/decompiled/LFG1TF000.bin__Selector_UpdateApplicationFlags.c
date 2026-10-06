/* Ghidra analysis output; verify against original SH instructions. */

/* WARNING: Removing unreachable block (ram,0x0002260e) */
/* WARNING: Removing unreachable block (ram,0x000226a6) */
/* 88B4..B7 feed9314 bit0,9317 bit2,9314 bit1,9316 bit2. Updates class8080 through22D08. Physical
   input names not yet proven. Also5120 cases verify89A4 nonzero ->9316bit0 via22CFE;
   completeinput25 producer/manager chain intcu-source-selection.txt. */

void Selector_UpdateApplicationFlags(void)

{
  char cVar1;
  char cVar2;
  char cVar3;
  char cVar4;
  bool bVar5;
  bool bVar6;
  bool bVar7;
  bool bVar8;
  bool bVar9;
  bool bVar10;
  bool bVar11;
  undefined *puVar12;
  undefined *puVar13;
  char cVar14;
  char cVar15;
  char cVar16;
  char cVar17;
  byte bVar18;
  char cVar19;
  byte bVar20;
  byte *pbVar21;
  undefined4 uVar22;
  byte *pbVar23;
  uint local_40;
  
  (*(code *)PTR_FUN_00022500)();
  bVar9 = false;
  if ((*PTR_DAT_00022504 & 1) == 0) {
    *PTR_DAT_00022508 = 0;
  }
  cVar1 = *PTR_Selector_FilteredInputZero_0002250c;
  cVar2 = *PTR_DAT_00022510;
  cVar14 = Selector_CombineInputsZeroAndTwo();
  cVar3 = *PTR_Selector_FilteredInputTwo_00022514;
  cVar4 = *PTR_DAT_00022518;
  cVar15 = (*(code *)PTR_FUN_0002251c)();
  cVar16 = (*(code *)PTR_FUN_00022520)();
  cVar17 = (*(code *)PTR_FUN_00022524)();
  bVar18 = (*(code *)PTR_FUN_00022528)();
  cVar19 = (*(code *)PTR_SourceInput_GetChannel25_0002252c)();
  pbVar21 = (byte *)(int)DAT_000224fc;
  if (cVar1 == '\0') {
    bVar20 = *pbVar21 & 0x7f;
  }
  else {
    bVar20 = *pbVar21 | 0x80;
  }
  *pbVar21 = bVar20;
  if (cVar2 == '\0') {
    bVar20 = *pbVar21 & 0xfe;
  }
  else {
    bVar20 = *pbVar21 | 1;
  }
  *pbVar21 = bVar20;
  if (cVar14 == '\0') {
    bVar20 = *pbVar21 & 0xfd;
  }
  else {
    bVar20 = *pbVar21 | 2;
  }
  *pbVar21 = bVar20;
  pbVar23 = (byte *)(int)DAT_000224fe;
  if (cVar3 == '\0') {
    bVar20 = *pbVar23 & 0xfe;
  }
  else {
    bVar20 = *pbVar23 | 1;
  }
  *pbVar23 = bVar20;
  if (cVar4 == '\0') {
    bVar20 = *pbVar21 & 0xfb;
  }
  else {
    bVar20 = *pbVar21 | 4;
  }
  *pbVar21 = bVar20;
  if (cVar15 == '\0') {
    bVar20 = *pbVar21 & 0xf7;
  }
  else {
    bVar20 = *pbVar21 | 8;
  }
  *pbVar21 = bVar20;
  if (cVar16 == '\0') {
    bVar20 = *pbVar21 & 0xef;
  }
  else {
    bVar20 = *pbVar21 | 0x10;
  }
  *pbVar21 = bVar20;
  if (cVar17 == '\0') {
    bVar20 = *pbVar21 & 0xdf;
  }
  else {
    bVar20 = *pbVar21 | 0x20;
  }
  *pbVar21 = bVar20;
  if (bVar18 == 0) {
    bVar20 = *pbVar21 & 0xbf;
  }
  else {
    bVar20 = *pbVar21 | 0x40;
  }
  *pbVar21 = bVar20;
  puVar12 = PTR_Selector_ApplicationFlags16_00022704;
  if ((cVar17 == '\0') && (bVar18 == 1)) {
    bVar18 = 0;
  }
  if (cVar19 == '\0') {
    bVar20 = *PTR_Selector_ApplicationFlags16_00022704 & 0xfe;
  }
  else {
    bVar20 = *PTR_Selector_ApplicationFlags16_00022704 | 1;
  }
  *PTR_Selector_ApplicationFlags16_00022704 = bVar20;
  puVar13 = PTR_DAT_00022708;
  if (cVar1 == '\0') {
    bVar20 = *PTR_DAT_00022708 & 0xfe;
  }
  else {
    bVar20 = *PTR_DAT_00022708 | 1;
  }
  *PTR_DAT_00022708 = bVar20;
  if (cVar2 == '\0') {
    bVar20 = puVar12[1] & 0xfb;
  }
  else {
    bVar20 = puVar12[1] | 4;
  }
  puVar12[1] = bVar20;
  if (cVar14 == '\0') {
    bVar20 = puVar12[1] & 0xf7;
  }
  else {
    bVar20 = puVar12[1] | 8;
  }
  puVar12[1] = bVar20;
  if (cVar3 == '\0') {
    bVar20 = *puVar13 & 0xfd;
  }
  else {
    bVar20 = *puVar13 | 2;
  }
  *puVar13 = bVar20;
  if (cVar4 == '\0') {
    bVar20 = *puVar12 & 0xfb;
  }
  else {
    bVar20 = *puVar12 | 4;
  }
  *puVar12 = bVar20;
  *puVar12 = *puVar12 & 0xf7;
  if (cVar16 == '\0') {
    bVar20 = *puVar12 & 0xef;
  }
  else {
    bVar20 = *puVar12 | 0x10;
  }
  *puVar12 = bVar20;
  if (cVar17 == '\0') {
    bVar20 = *puVar12 & 0xdf;
  }
  else {
    bVar20 = *puVar12 | 0x20;
  }
  local_40 = (uint)bVar18;
  *puVar12 = bVar20;
  puVar12 = PTR_FUN_00022710;
  if (local_40 == 0) {
    bVar18 = *PTR_DAT_0002270c & 0xef;
  }
  else {
    bVar18 = *PTR_DAT_0002270c | 0x10;
  }
  *PTR_DAT_0002270c = bVar18;
  (*(code *)puVar12)();
  if ((((cVar2 == '\0') && (cVar14 == '\0')) && (cVar16 == '\0')) &&
     ((cVar17 == '\0' && (local_40 == 0)))) {
    uVar22 = 6;
  }
  else {
    uVar22 = 0;
    if (cVar2 == '\x01') {
      uVar22 = 0xffffffff;
    }
    if (cVar17 == '\x01') {
      uVar22 = 2;
    }
    if (cVar16 == '\x01') {
      uVar22 = 3;
    }
    if (cVar4 == '\x01') {
      uVar22 = 6;
    }
    if (local_40 == 1) {
      uVar22 = 1;
    }
  }
  uVar22 = (*(code *)PTR_FUN_00022714)(uVar22);
  bVar18 = (*(code *)PTR_FUN_00022718)(uVar22);
  TransmissionStateClass = bVar18;
  (*(code *)PTR_FUN_0002271c)();
  bVar5 = false;
  bVar6 = false;
  bVar7 = false;
  bVar10 = false;
  bVar11 = false;
  bVar8 = false;
  if (bVar18 == 0xff) {
    bVar5 = true;
  }
  else if (bVar18 == 0) {
    bVar6 = true;
  }
  else if (bVar18 == 1) {
    bVar7 = true;
  }
  else if (bVar18 == 2) {
    bVar8 = true;
  }
  else if (bVar18 == 3) {
    bVar10 = true;
  }
  else if (bVar18 == 4) {
    local_40 = 0x1000000;
  }
  else if (bVar18 == 5) {
    bVar11 = true;
  }
  else {
    bVar9 = true;
  }
  uVar22 = (*(code *)PTR_FUN_000227ec)();
  if (bVar5) {
    bVar18 = puVar13[1] | 1;
  }
  else {
    bVar18 = puVar13[1] & 0xfe;
  }
  puVar13[1] = bVar18;
  if (bVar6) {
    bVar18 = puVar13[1] | 2;
  }
  else {
    bVar18 = puVar13[1] & 0xfd;
  }
  puVar13[1] = bVar18;
  if (bVar7) {
    bVar18 = puVar13[1] | 0x80;
  }
  else {
    bVar18 = puVar13[1] & 0x7f;
  }
  puVar13[1] = bVar18;
  if (bVar8) {
    bVar18 = puVar13[1] | 0x40;
  }
  else {
    bVar18 = puVar13[1] & 0xbf;
  }
  puVar13[1] = bVar18;
  if (bVar10) {
    bVar18 = puVar13[1] | 0x20;
  }
  else {
    bVar18 = puVar13[1] & 0xdf;
  }
  puVar13[1] = bVar18;
  if (local_40._0_1_ == '\0') {
    bVar18 = puVar13[1] & 0xef;
  }
  else {
    bVar18 = puVar13[1] | 0x10;
  }
  puVar13[1] = bVar18;
  if (bVar11) {
    bVar18 = puVar13[1] | 8;
  }
  else {
    bVar18 = puVar13[1] & 0xf7;
  }
  puVar13[1] = bVar18;
  puVar12 = PTR_FUN_000227f0;
  if (bVar9) {
    bVar18 = puVar13[1] | 4;
  }
  else {
    bVar18 = puVar13[1] & 0xfb;
  }
  puVar13[1] = bVar18;
  (*(code *)puVar12)(uVar22);
  FUN_000227f8();
  (*(code *)PTR_FUN_000227f4)();
  return;
}

