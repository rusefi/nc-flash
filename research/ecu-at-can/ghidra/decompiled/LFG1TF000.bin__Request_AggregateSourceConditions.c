/* Ghidra analysis output; verify against original SH instructions. */

/* Original aggregate produces916Fbit0
   from92C6bits2/5,92CAbits0/1,92CCbits1/2,92CDbits3/4,or92D0bit2CLEAR.1280 cases,152 perturbations
   and9 cancellation lifecycles verified; other outputs not newly fully specified. */

void Request_AggregateSourceConditions(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined *puVar5;
  byte bVar6;
  uint uVar7;
  byte *pbVar8;
  
  if (((((PTR_ApplicationFaultFlags92C6_0001ff20[1] & 1) == 1) ||
       ((PTR_ApplicationFaultFlags92C6_0001ff20[1] & 2) != 0)) ||
      ((PTR_ApplicationFaultFlags92C6_0001ff20[1] & 4) != 0)) ||
     (((PTR_ApplicationFaultFlags92C6_0001ff20[1] & 8) != 0 ||
      ((PTR_ApplicationFaultFlags92C6_0001ff20[1] & 0x10) != 0)))) {
    bVar6 = *PTR_DAT_0001ff1c | 1;
  }
  else {
    bVar6 = *PTR_DAT_0001ff1c & 0xfe;
  }
  *PTR_DAT_0001ff1c = bVar6;
  if (*PTR_DAT_0001ff28 == '\x01') {
    bVar6 = *PTR_DAT_0001ff24 & 0xbf;
  }
  else {
    bVar6 = *PTR_DAT_0001ff24 | 0x40;
  }
  *PTR_DAT_0001ff24 = bVar6;
  puVar3 = PTR_DAT_0001ff30;
  puVar2 = PTR_DAT_0001ff2c;
  if ((PTR_DAT_0001ff2c[1] & 4) == 0) {
    bVar6 = PTR_DAT_0001ff30[1] & 0xf7;
  }
  else {
    bVar6 = PTR_DAT_0001ff30[1] | 8;
  }
  PTR_DAT_0001ff30[1] = bVar6;
  if ((puVar2[1] & 2) == 0) {
    bVar6 = puVar3[1] & 0xfb;
  }
  else {
    bVar6 = puVar3[1] | 4;
  }
  puVar3[1] = bVar6;
  if ((*PTR_DAT_0001ff34 & 1) == 0) {
    bVar6 = puVar3[1] & 0xfd;
  }
  else {
    bVar6 = puVar3[1] | 2;
  }
  puVar3[1] = bVar6;
  if ((*PTR_DAT_0001ff24 & 0x40) == 0) {
    bVar6 = puVar3[1] & 0xfe;
  }
  else {
    bVar6 = puVar3[1] | 1;
  }
  puVar3[1] = bVar6;
  puVar2 = PTR_DAT_0001ff38;
  if ((*PTR_DAT_0001ff38 & 4) == 0) {
    bVar6 = puVar3[2] & 0x7f;
  }
  else {
    bVar6 = puVar3[2] | 0x80;
  }
  puVar3[2] = bVar6;
  if ((*puVar2 & 0x20) == 0) {
    bVar6 = puVar3[2] & 0xbf;
  }
  else {
    bVar6 = puVar3[2] | 0x40;
  }
  puVar3[2] = bVar6;
  if ((*PTR_DAT_0001ff1c & 1) == 0) {
    bVar6 = puVar3[2] & 0xdf;
  }
  else {
    bVar6 = puVar3[2] | 0x20;
  }
  puVar3[2] = bVar6;
  puVar1 = PTR_ApplicationFaultFlags92C6_0001ff20;
  if ((*PTR_ApplicationFaultFlags92C6_0001ff20 & 1) == 0) {
    bVar6 = puVar3[2] & 0xef;
  }
  else {
    bVar6 = puVar3[2] | 0x10;
  }
  puVar3[2] = bVar6;
  if (((int)(char)puVar1[1] & 0x80U) == 0) {
    bVar6 = puVar3[2] & 0xf7;
  }
  else {
    bVar6 = puVar3[2] | 8;
  }
  puVar3[2] = bVar6;
  if ((puVar1[1] & 0x40) == 0) {
    bVar6 = puVar3[2] & 0xfb;
  }
  else {
    bVar6 = puVar3[2] | 4;
  }
  puVar3[2] = bVar6;
  if ((puVar1[1] & 0x20) == 0) {
    bVar6 = puVar3[2] & 0xfd;
  }
  else {
    bVar6 = puVar3[2] | 2;
  }
  puVar3[2] = bVar6;
  if ((*puVar2 & 8) == 0) {
    bVar6 = puVar3[2] & 0xfe;
  }
  else {
    bVar6 = puVar3[2] | 1;
  }
  puVar3[2] = bVar6;
  puVar2 = PTR_DAT_0001ff3c;
  if ((PTR_DAT_0001ff3c[1] & 1) == 0) {
    bVar6 = puVar3[3] & 0x7f;
  }
  else {
    bVar6 = puVar3[3] | 0x80;
  }
  puVar3[3] = bVar6;
  if (((int)(char)*puVar1 & 0x80U) == 0) {
    bVar6 = puVar3[3] & 0xbf;
  }
  else {
    bVar6 = puVar3[3] | 0x40;
  }
  puVar3[3] = bVar6;
  if ((*puVar1 & 0x40) == 0) {
    bVar6 = puVar3[3] & 0xdf;
  }
  else {
    bVar6 = puVar3[3] | 0x20;
  }
  puVar3[3] = bVar6;
  if ((*puVar1 & 4) == 0) {
    bVar6 = puVar3[3] & 0xef;
  }
  else {
    bVar6 = puVar3[3] | 0x10;
  }
  puVar3[3] = bVar6;
  if ((*puVar1 & 2) == 0) {
    bVar6 = puVar3[3] & 0xf7;
  }
  else {
    bVar6 = puVar3[3] | 8;
  }
  puVar3[3] = bVar6;
  if ((*puVar1 & 0x20) == 0) {
    bVar6 = puVar3[3] & 0xfb;
  }
  else {
    bVar6 = puVar3[3] | 4;
  }
  puVar3[3] = bVar6;
  if ((*puVar1 & 0x10) == 0) {
    bVar6 = puVar3[3] & 0xfd;
  }
  else {
    bVar6 = puVar3[3] | 2;
  }
  puVar3[3] = bVar6;
  if ((*PTR_DAT_00020124 & 1) == 0) {
    bVar6 = puVar3[3] & 0xfe;
  }
  else {
    bVar6 = puVar3[3] | 1;
  }
  puVar3[3] = bVar6;
  puVar4 = PTR_DAT_00020128;
  if ((puVar2[1] & 4) == 0) {
    bVar6 = PTR_DAT_00020128[1] & 0xef;
  }
  else {
    bVar6 = PTR_DAT_00020128[1] | 0x10;
  }
  PTR_DAT_00020128[1] = bVar6;
  if ((*puVar2 & 4) == 0) {
    bVar6 = puVar4[1] & 0xf7;
  }
  else {
    bVar6 = puVar4[1] | 8;
  }
  puVar4[1] = bVar6;
  if ((*PTR_DAT_0002012c & 4) == 0) {
    bVar6 = puVar4[1] | 4;
  }
  else {
    bVar6 = puVar4[1] & 0xfb;
  }
  puVar4[1] = bVar6;
  if ((*PTR_ApplicationFaultFlags92D5_00020130 & 0x40) == 0) {
    bVar6 = puVar4[1] & 0xfd;
  }
  else {
    bVar6 = puVar4[1] | 2;
  }
  puVar4[1] = bVar6;
  if ((*puVar1 & 8) == 0) {
    bVar6 = puVar4[1] & 0xfe;
  }
  else {
    bVar6 = puVar4[1] | 1;
  }
  puVar4[1] = bVar6;
  puVar1 = PTR_DAT_00020134;
  if ((*PTR_DAT_00020134 & 1) == 0) {
    bVar6 = puVar4[2] & 0x7f;
  }
  else {
    bVar6 = puVar4[2] | 0x80;
  }
  puVar4[2] = bVar6;
  if ((puVar1[1] & 1) == 0) {
    bVar6 = puVar4[2] & 0xbf;
  }
  else {
    bVar6 = puVar4[2] | 0x40;
  }
  puVar4[2] = bVar6;
  puVar5 = PTR_DAT_00020138;
  if (((int)(char)*PTR_DAT_00020138 & 0x80U) == 0) {
    bVar6 = puVar4[2] & 0xdf;
  }
  else {
    bVar6 = puVar4[2] | 0x20;
  }
  puVar4[2] = bVar6;
  if ((*puVar5 & 0x40) == 0) {
    bVar6 = puVar4[2] & 0xef;
  }
  else {
    bVar6 = puVar4[2] | 0x10;
  }
  puVar4[2] = bVar6;
  if (((int)(char)puVar1[1] & 0x80U) == 0) {
    bVar6 = puVar4[2] & 0xf7;
  }
  else {
    bVar6 = puVar4[2] | 8;
  }
  puVar4[2] = bVar6;
  if ((puVar2[1] & 2) == 0) {
    bVar6 = puVar4[2] & 0xfb;
  }
  else {
    bVar6 = puVar4[2] | 4;
  }
  puVar4[2] = bVar6;
  if ((puVar1[1] & 0x10) == 0) {
    bVar6 = puVar4[2] & 0xfd;
  }
  else {
    bVar6 = puVar4[2] | 2;
  }
  puVar4[2] = bVar6;
  if ((puVar1[1] & 8) == 0) {
    bVar6 = puVar4[2] & 0xfe;
  }
  else {
    bVar6 = puVar4[2] | 1;
  }
  puVar4[2] = bVar6;
  if (((int)(char)puVar2[1] & 0x80U) == 0) {
    bVar6 = puVar4[3] & 0x7f;
  }
  else {
    bVar6 = puVar4[3] | 0x80;
  }
  puVar4[3] = bVar6;
  if ((puVar2[1] & 0x40) == 0) {
    bVar6 = puVar4[3] & 0xbf;
  }
  else {
    bVar6 = puVar4[3] | 0x40;
  }
  puVar4[3] = bVar6;
  if ((*puVar1 & 0x20) == 0) {
    bVar6 = puVar4[3] & 0xdf;
  }
  else {
    bVar6 = puVar4[3] | 0x20;
  }
  puVar4[3] = bVar6;
  if ((*puVar5 & 0x10) == 0) {
    bVar6 = puVar4[3] & 0xef;
  }
  else {
    bVar6 = puVar4[3] | 0x10;
  }
  puVar4[3] = bVar6;
  if ((*puVar1 & 4) == 0) {
    bVar6 = puVar4[3] & 0xf7;
  }
  else {
    bVar6 = puVar4[3] | 8;
  }
  puVar4[3] = bVar6;
  if ((*puVar5 & 2) == 0) {
    bVar6 = puVar4[3] & 0xfb;
  }
  else {
    bVar6 = puVar4[3] | 4;
  }
  puVar4[3] = bVar6;
  if ((*puVar1 & 2) == 0) {
    bVar6 = puVar4[3] & 0xfd;
  }
  else {
    bVar6 = puVar4[3] | 2;
  }
  puVar4[3] = bVar6;
  if ((*puVar5 & 1) == 0) {
    bVar6 = puVar4[3] & 0xfe;
  }
  else {
    bVar6 = puVar4[3] | 1;
  }
  puVar4[3] = bVar6;
  *(undefined4 *)(int)DAT_000202c8 = *(undefined4 *)puVar3;
  uVar7 = *(uint *)puVar4;
  *(uint *)(int)DAT_000202ca = uVar7;
  (*(code *)PTR_Pack_MsbRelativeBitfield_000202e0)();
  (*(code *)PTR_Pack_MsbRelativeBitfield_000202e0)();
  (*(code *)PTR_Pack_MsbRelativeBitfield_000202e0)();
  (*(code *)PTR_Pack_MsbRelativeBitfield_000202e0)();
  (*(code *)PTR_Pack_MsbRelativeBitfield_000202e0)();
  (*(code *)PTR_Pack_MsbRelativeBitfield_000202e0)();
  (*(code *)PTR_Pack_MsbRelativeBitfield_000202e0)();
  (*(code *)PTR_Pack_MsbRelativeBitfield_000202e0)();
  (*(code *)PTR_Pack_MsbRelativeBitfield_000202e0)();
  (*(code *)PTR_Pack_MsbRelativeBitfield_000202e0)();
  (*(code *)PTR_Pack_MsbRelativeBitfield_000202e0)();
  pbVar8 = PTR_Request_CancellationFlags_00020308;
  (*(code *)PTR_Pack_MsbRelativeBitfield_000202e0)();
  (*(code *)PTR_Pack_MsbRelativeBitfield_000202e0)();
  (*(code *)PTR_Pack_MsbRelativeBitfield_000202e0)();
  (*(code *)PTR_Pack_MsbRelativeBitfield_000202e0)();
  (*(code *)PTR_Pack_MsbRelativeBitfield_000202e0)();
  (*(code *)PTR_Pack_MsbRelativeBitfield_00020490)();
  (*(code *)PTR_Pack_MsbRelativeBitfield_00020490)();
  (*(code *)PTR_Pack_MsbRelativeBitfield_00020490)();
  *pbVar8 = *pbVar8 & 0xf7;
  (*(code *)PTR_Pack_MsbRelativeBitfield_00020490)();
  (*(code *)PTR_Pack_MsbRelativeBitfield_00020490)();
  (*(code *)PTR_Pack_MsbRelativeBitfield_00020490)();
  (*(code *)PTR_Pack_MsbRelativeBitfield_00020490)();
  (*(code *)PTR_Pack_MsbRelativeBitfield_00020490)();
  (*(code *)PTR_Pack_MsbRelativeBitfield_00020490)();
  (*(code *)PTR_Pack_MsbRelativeBitfield_00020490)();
  (*(code *)PTR_Pack_MsbRelativeBitfield_00020490)();
  (*(code *)PTR_Pack_MsbRelativeBitfield_00020490)();
  (*(code *)PTR_Pack_MsbRelativeBitfield_00020490)();
  (*(code *)PTR_Pack_MsbRelativeBitfield_00020490)();
  (*(code *)PTR_Pack_MsbRelativeBitfield_00020490)(uVar7 & (uint)PTR_DAT_000204bc);
  return;
}

