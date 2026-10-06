/* Ghidra analysis output; verify against original SH instructions. */

/* A964 bit3 ->92CD bit5; A964 bit2 ->92CD bit6, forcing CAN231 nibbles F. Paired execution
   verified. */

void Diagnostic_PublishApplicationFlags(void)

{
  byte bVar1;
  byte bVar2;
  byte bVar3;
  byte bVar4;
  byte bVar5;
  byte bVar6;
  byte bVar7;
  char cVar8;
  char cVar9;
  undefined *puVar10;
  undefined *puVar11;
  undefined *puVar12;
  int iVar13;
  byte bVar14;
  byte bVar15;
  bool bVar16;
  char acStack_1000c [65536];
  char local_c [4];
  
  puVar10 = PTR_DAT_00021fa8;
  iVar13 = (int)DAT_00021dd6;
  local_c[DAT_00021dd8 + iVar13] = -(((PTR_DAT_00021dec[0x2c] & 8) == 0) + -1);
  local_c[DAT_00021dda + iVar13] = -(((PTR_DAT_00021dec[0x2c] & 4) == 0) + -1);
  local_c[DAT_00021ddc + iVar13] = -(((PTR_DAT_00021dec[0x2a] & 4) == 0) + -1);
  local_c[DAT_00021dde + iVar13] = -(((PTR_DAT_00021dec[0x2b] & 4) == 0) + -1);
  (&stack0x00000048)[iVar13] = -(((PTR_DAT_00021dec[0xc] & 8) == 0) + -1);
  local_c[DAT_00021de0 + iVar13] = -(((PTR_DAT_00021dec[0xc] & 4) == 0) + -1);
  local_c[DAT_00021de2 + iVar13] = -(((PTR_DAT_00021dec[1] & 8) == 0) + -1);
  local_c[DAT_00021de4 + iVar13] = -(((PTR_DAT_00021dec[2] & 8) == 0) + -1);
  local_c[DAT_00021de6 + iVar13] = -(((PTR_DAT_00021dec[5] & 8) == 0) + -1);
  local_c[DAT_00021de8 + iVar13] = -(((PTR_DAT_00021dec[3] & 8) == 0) + -1);
  (&stack0x00000070)[iVar13] = -(((PTR_DAT_00021dec[4] & 8) == 0) + -1);
  bVar4 = PTR_DAT_00021dec[6];
  bVar15 = PTR_DAT_00021dec[0x2f];
  bVar5 = PTR_DAT_00021dec[7];
  bVar1 = PTR_DAT_00021dec[0x30];
  bVar6 = PTR_DAT_00021dec[8];
  bVar2 = PTR_DAT_00021dec[0x31];
  bVar7 = PTR_DAT_00021dec[9];
  bVar3 = PTR_DAT_00021dec[0x32];
  (&stack0x0000006c)[iVar13] = -(((PTR_DAT_00021dec[10] & 8) == 0) + -1);
  (&stack0x00000068)[iVar13] = -(((PTR_DAT_00021dec[10] & 4) == 0) + -1);
  (&stack0x00000064)[iVar13] = -(((PTR_DAT_00021dec[0xb] & 8) == 0) + -1);
  (&stack0x00000060)[iVar13] = -(((PTR_DAT_00021dec[0xb] & 4) == 0) + -1);
  (&stack0x0000005c)[iVar13] = -(((PTR_DAT_00021dec[0xd] & 8) == 0) + -1);
  (&stack0x00000058)[iVar13] = -(((PTR_DAT_00021dec[0xd] & 4) == 0) + -1);
  (&stack0x00000054)[iVar13] = -(((PTR_DAT_00021dec[0x1d] & 8) == 0) + -1);
  (&stack0x00000050)[iVar13] = -(((PTR_DAT_00021dec[0x1e] & 8) == 0) + -1);
  *(undefined **)(local_c + iVar13) = PTR_DAT_00021fa4 + 5;
  (&stack0x0000004c)[iVar13] = -(((PTR_DAT_00021fa4[5] & 8) == 0) + -1);
  (&stack0x00000040)[iVar13] = -(((**(byte **)(local_c + iVar13) & 4) == 0) + -1);
  *(undefined **)(local_c + iVar13) = PTR_DAT_00021fa4 + 3;
  (&stack0xfffffff8)[iVar13] = -(((PTR_DAT_00021fa4[3] & 8) == 0) + -1);
  (&stack0xfffffffc)[iVar13] = -(((**(byte **)(local_c + iVar13) & 4) == 0) + -1);
  *(undefined **)(local_c + iVar13) = PTR_DAT_00021dec + 0x25;
  (&stack0x00000000)[iVar13] = -(((PTR_DAT_00021dec[0x25] & 8) == 0) + -1);
  (&stack0x00000004)[iVar13] = -(((**(byte **)(local_c + iVar13) & 4) == 0) + -1);
  *(undefined **)(local_c + iVar13) = PTR_DAT_00021fa4 + 1;
  (&stack0x00000018)[iVar13] = -(((PTR_DAT_00021fa4[1] & 8) == 0) + -1);
  (&stack0x00000014)[iVar13] = -(((**(byte **)(local_c + iVar13) & 4) == 0) + -1);
  *(undefined **)(local_c + iVar13) = PTR_DAT_00021fa4 + 4;
  (&stack0x00000008)[iVar13] = -(((PTR_DAT_00021fa4[4] & 8) == 0) + -1);
  (&stack0x0000000c)[iVar13] = -(((**(byte **)(local_c + iVar13) & 4) == 0) + -1);
  *(undefined **)(local_c + iVar13) = PTR_DAT_00021fa4 + 2;
  (&stack0x00000010)[iVar13] = -(((PTR_DAT_00021fa4[2] & 8) == 0) + -1);
  (&stack0x0000001c)[iVar13] = -(((**(byte **)(local_c + iVar13) & 4) == 0) + -1);
  (&stack0x00000020)[iVar13] = -(((PTR_DAT_00021dec[0x1f] & 8) == 0) + -1);
  (&stack0x0000003c)[iVar13] = -(((PTR_DAT_00021dec[0x1f] & 4) == 0) + -1);
  (&stack0x00000038)[iVar13] = -(((PTR_DAT_00021dec[0x20] & 8) == 0) + -1);
  (&stack0x00000034)[iVar13] = -(((PTR_DAT_00021dec[0x20] & 4) == 0) + -1);
  (&stack0x00000030)[iVar13] = -(((PTR_DAT_00021dec[0x21] & 8) == 0) + -1);
  (&stack0x0000002c)[iVar13] = -(((PTR_DAT_00021dec[0x21] & 4) == 0) + -1);
  (&stack0x00000028)[iVar13] = -(((PTR_DAT_00021dec[0x22] & 8) == 0) + -1);
  (&stack0x00000024)[iVar13] = -(((PTR_DAT_00021dec[0x22] & 4) == 0) + -1);
  local_c[iVar13] = -(((PTR_DAT_00021dec[0x23] & 8) == 0) + -1);
  (&stack0x00000044)[iVar13] = -(((PTR_DAT_00021dec[0x23] & 4) == 0) + -1);
  if (local_c[DAT_00021fa2 + iVar13] == '\0') {
    bVar14 = *PTR_DAT_00021fa8 & 0xfb;
  }
  else {
    bVar14 = *PTR_DAT_00021fa8 | 4;
  }
  *PTR_DAT_00021fa8 = bVar14;
  if (local_c[DAT_00022080 + iVar13] == '\0') {
    bVar14 = *puVar10 & 0xdf;
  }
  else {
    bVar14 = *puVar10 | 0x20;
  }
  *puVar10 = bVar14;
  if (local_c[DAT_00022082 + iVar13] == '\0') {
    bVar14 = *puVar10 & 0xf7;
  }
  else {
    bVar14 = *puVar10 | 8;
  }
  *puVar10 = bVar14;
  if (local_c[DAT_00022084 + iVar13] == '\0') {
    bVar14 = *puVar10 & 0xef;
  }
  else {
    bVar14 = *puVar10 | 0x10;
  }
  *puVar10 = bVar14;
  puVar10 = PTR_DAT_00022090;
  if ((&stack0x00000048)[iVar13] == '\0') {
    bVar14 = PTR_DAT_00022090[1] & 0xdf;
  }
  else {
    bVar14 = PTR_DAT_00022090[1] | 0x20;
  }
  PTR_DAT_00022090[1] = bVar14;
  if (local_c[DAT_00022086 + iVar13] == '\0') {
    bVar14 = puVar10[1] & 0xbf;
  }
  else {
    bVar14 = puVar10[1] | 0x40;
  }
  puVar10[1] = bVar14;
  puVar11 = PTR_ApplicationFaultFlags92C6_00022094;
  if (local_c[DAT_00022088 + iVar13] == '\0') {
    bVar14 = PTR_ApplicationFaultFlags92C6_00022094[1] & 0xfe;
  }
  else {
    bVar14 = PTR_ApplicationFaultFlags92C6_00022094[1] | 1;
  }
  PTR_ApplicationFaultFlags92C6_00022094[1] = bVar14;
  if (local_c[DAT_0002208a + iVar13] == '\0') {
    bVar14 = puVar11[1] & 0xfd;
  }
  else {
    bVar14 = puVar11[1] | 2;
  }
  puVar11[1] = bVar14;
  if (local_c[DAT_0002208c + iVar13] == '\0') {
    bVar14 = puVar11[1] & 0xfb;
  }
  else {
    bVar14 = puVar11[1] | 4;
  }
  puVar11[1] = bVar14;
  if (local_c[DAT_0002208e + iVar13] == '\0') {
    bVar14 = puVar11[1] & 0xf7;
  }
  else {
    bVar14 = puVar11[1] | 8;
  }
  puVar11[1] = bVar14;
  if ((&stack0x00000070)[iVar13] == '\0') {
    bVar14 = puVar11[1] & 0xef;
  }
  else {
    bVar14 = puVar11[1] | 0x10;
  }
  puVar11[1] = bVar14;
  if ((bVar4 & 8) == 0 && (bVar15 & 4) == 0) {
    bVar15 = puVar11[1] & 0xdf;
  }
  else {
    bVar15 = puVar11[1] | 0x20;
  }
  puVar11[1] = bVar15;
  if ((bVar5 & 8) == 0 && (bVar1 & 4) == 0) {
    bVar15 = puVar11[1] & 0xbf;
  }
  else {
    bVar15 = puVar11[1] | 0x40;
  }
  puVar11[1] = bVar15;
  if ((bVar6 & 8) == 0 && (bVar2 & 4) == 0) {
    bVar15 = puVar11[1] & 0x7f;
  }
  else {
    bVar15 = puVar11[1] | 0x80;
  }
  puVar11[1] = bVar15;
  if ((bVar7 & 8) == 0 && (bVar3 & 4) == 0) {
    bVar15 = *puVar11 & 0xfe;
  }
  else {
    bVar15 = *puVar11 | 1;
  }
  *puVar11 = bVar15;
  if ((&stack0x0000006c)[iVar13] == '\0') {
    bVar15 = *puVar11 & 0xfd;
  }
  else {
    bVar15 = *puVar11 | 2;
  }
  *puVar11 = bVar15;
  if ((&stack0x00000068)[iVar13] == '\0') {
    bVar15 = *puVar11 & 0xfb;
  }
  else {
    bVar15 = *puVar11 | 4;
  }
  *puVar11 = bVar15;
  *puVar11 = *puVar11 & 0xf7;
  if ((&stack0x00000064)[iVar13] == '\0') {
    bVar15 = *puVar11 & 0xef;
  }
  else {
    bVar15 = *puVar11 | 0x10;
  }
  *puVar11 = bVar15;
  if ((&stack0x00000060)[iVar13] == '\0') {
    bVar15 = *puVar11 & 0xdf;
  }
  else {
    bVar15 = *puVar11 | 0x20;
  }
  *puVar11 = bVar15;
  if ((&stack0x0000005c)[iVar13] == '\0') {
    bVar15 = *puVar11 & 0xbf;
  }
  else {
    bVar15 = *puVar11 | 0x40;
  }
  *puVar11 = bVar15;
  if ((&stack0x00000058)[iVar13] == '\0') {
    bVar15 = *puVar11 & 0x7f;
  }
  else {
    bVar15 = *puVar11 | 0x80;
  }
  *puVar11 = bVar15;
  puVar12 = PTR_DAT_000222a0;
  puVar11 = PTR_DAT_0002229c;
  PTR_DAT_0002229c[1] = PTR_DAT_0002229c[1] & 0xfe;
  if ((&stack0x00000054)[iVar13] == '\0') {
    bVar15 = puVar12[1] & 0xfd;
  }
  else {
    bVar15 = puVar12[1] | 2;
  }
  puVar12[1] = bVar15;
  if ((&stack0x00000050)[iVar13] == '\0') {
    bVar15 = puVar12[1] & 0xfb;
  }
  else {
    bVar15 = puVar12[1] | 4;
  }
  puVar12[1] = bVar15;
  puVar12 = PTR_DAT_000222a4;
  puVar11[1] = puVar11[1] & 0xfb;
  puVar11[1] = puVar11[1] & 0xf7;
  puVar11[1] = puVar11[1] & 0xef;
  puVar11[1] = puVar11[1] & 0xdf;
  puVar12[1] = puVar12[1] & 0xf7;
  *puVar11 = *puVar11 & 0xfe;
  if ((&stack0x0000004c)[iVar13] == '\0') {
    bVar15 = puVar11[1] & 0xfd;
  }
  else {
    bVar15 = puVar11[1] | 2;
  }
  puVar11[1] = bVar15;
  if ((&stack0x00000040)[iVar13] == '\0') {
    bVar15 = puVar10[1] & 0x7f;
  }
  else {
    bVar15 = puVar10[1] | 0x80;
  }
  puVar10[1] = bVar15;
  if ((&stack0xfffffff8)[iVar13] == '\0') {
    bVar15 = puVar11[1] & 0xbf;
  }
  else {
    bVar15 = puVar11[1] | 0x40;
  }
  puVar11[1] = bVar15;
  if ((&stack0xfffffffc)[iVar13] == '\0') {
    bVar15 = puVar11[1] & 0x7f;
  }
  else {
    bVar15 = puVar11[1] | 0x80;
  }
  puVar11[1] = bVar15;
  if ((&stack0x00000000)[iVar13] == '\0') {
    bVar15 = puVar10[1] & 0xf7;
  }
  else {
    bVar15 = puVar10[1] | 8;
  }
  puVar10[1] = bVar15;
  if ((&stack0x00000004)[iVar13] == '\0') {
    bVar15 = puVar10[1] & 0xef;
  }
  else {
    bVar15 = puVar10[1] | 0x10;
  }
  puVar10[1] = bVar15;
  cVar8 = (&stack0x00000008)[iVar13];
  if (cVar8 == '\0') {
    bVar15 = *puVar12 & 0xbf;
  }
  else {
    bVar15 = *puVar12 | 0x40;
  }
  *puVar12 = bVar15;
  if ((&stack0x0000000c)[iVar13] == '\0') {
    bVar15 = *puVar12 & 0x7f;
  }
  else {
    bVar15 = *puVar12 | 0x80;
  }
  *puVar12 = bVar15;
  cVar9 = (&stack0x00000010)[iVar13];
  if (cVar9 == '\0') {
    bVar15 = puVar10[1] & 0xfe;
  }
  else {
    bVar15 = puVar10[1] | 1;
  }
  puVar10[1] = bVar15;
  if ((&stack0x0000001c)[iVar13] == '\0') {
    bVar15 = *puVar10 & 0xfe;
  }
  else {
    bVar15 = *puVar10 | 1;
  }
  *puVar10 = bVar15;
  puVar10[1] = puVar10[1] & 0xfd;
  puVar10[1] = puVar10[1] & 0xfb;
  if ((&stack0x00000020)[iVar13] == '\0') {
    bVar15 = *puVar12 & 0xfe;
  }
  else {
    bVar15 = *puVar12 | 1;
  }
  *puVar12 = bVar15;
  if ((&stack0x0000003c)[iVar13] == '\0') {
    bVar15 = *puVar10 & 0xfd;
  }
  else {
    bVar15 = *puVar10 | 2;
  }
  *puVar10 = bVar15;
  if ((&stack0x00000038)[iVar13] == '\0') {
    bVar15 = *puVar12 & 0xfd;
  }
  else {
    bVar15 = *puVar12 | 2;
  }
  *puVar12 = bVar15;
  if ((&stack0x00000034)[iVar13] == '\0') {
    bVar15 = *puVar10 & 0xfb;
  }
  else {
    bVar15 = *puVar10 | 4;
  }
  *puVar10 = bVar15;
  if ((&stack0x00000030)[iVar13] == '\0') {
    bVar15 = *puVar12 & 0xfb;
  }
  else {
    bVar15 = *puVar12 | 4;
  }
  *puVar12 = bVar15;
  if ((&stack0x0000002c)[iVar13] == '\0') {
    bVar15 = *puVar10 & 0xf7;
  }
  else {
    bVar15 = *puVar10 | 8;
  }
  *puVar10 = bVar15;
  if ((&stack0x00000028)[iVar13] == '\0') {
    bVar15 = *puVar12 & 0xf7;
  }
  else {
    bVar15 = *puVar12 | 8;
  }
  *puVar12 = bVar15;
  if ((&stack0x00000024)[iVar13] == '\0') {
    bVar15 = *puVar10 & 0xef;
  }
  else {
    bVar15 = *puVar10 | 0x10;
  }
  *puVar10 = bVar15;
  if (local_c[iVar13] == '\0') {
    bVar15 = *puVar12 & 0xef;
  }
  else {
    bVar15 = *puVar12 | 0x10;
  }
  *puVar12 = bVar15;
  if ((&stack0x00000044)[iVar13] == '\0') {
    bVar15 = *puVar10 & 0xdf;
  }
  else {
    bVar15 = *puVar10 | 0x20;
  }
  *puVar10 = bVar15;
  *puVar12 = *puVar12 & 0xdf;
  *puVar10 = *puVar10 & 0xbf;
  if ((&stack0x00000018)[iVar13] == '\0') {
    bVar15 = puVar12[1] & 0xfd;
  }
  else {
    bVar15 = puVar12[1] | 2;
  }
  puVar12[1] = bVar15;
  if ((&stack0x00000014)[iVar13] == '\0') {
    bVar15 = *puVar10 & 0x7f;
  }
  else {
    bVar15 = *puVar10 | 0x80;
  }
  *puVar10 = bVar15;
  puVar11 = PTR_DAT_000223d8;
  puVar10 = PTR_DAT_000223d4;
  *PTR_DAT_000223d4 = *PTR_DAT_000223d4 & 0xef;
  *puVar11 = *puVar11 & 0xbf;
  *puVar10 = *puVar10 & 0xdf;
  *puVar10 = *puVar10 & 0xbf;
  *puVar10 = *puVar10 & 0x7f;
  bVar16 = false;
  if ((cVar9 == '\x01') || (cVar8 == '\x01')) {
    bVar16 = true;
  }
  if (bVar16) {
    bVar15 = PTR_DAT_000223dc[1] | 0x80;
  }
  else {
    bVar15 = PTR_DAT_000223dc[1] & 0x7f;
  }
  PTR_DAT_000223dc[1] = bVar15;
  (*(code *)PTR_FUN_0002240c)();
  return;
}

