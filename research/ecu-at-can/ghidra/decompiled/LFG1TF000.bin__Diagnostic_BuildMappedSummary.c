/* Ghidra analysis output; verify against original SH instructions. */

/* Maps group active flags and stored history to 51 bytes A958 onward; groups15/16 share index0C. */

void Diagnostic_BuildMappedSummary(void)

{
  byte bVar1;
  uint uVar2;
  char cVar3;
  byte *pbVar4;
  uint uVar5;
  byte local_54 [51];
  byte abStack_21 [5];
  
  for (pbVar4 = local_54; pbVar4 < abStack_21; pbVar4 = pbVar4 + 1) {
    *pbVar4 = *pbVar4 | 1;
    *pbVar4 = *pbVar4 & 0xfd;
    *pbVar4 = *pbVar4 & 0xfb;
    *pbVar4 = *pbVar4 & 0xf7;
    *pbVar4 = *pbVar4 & 0xef;
    *pbVar4 = *pbVar4 & 0xdf;
    *pbVar4 = *pbVar4 & 0xbf;
    *pbVar4 = *pbVar4 & 0x7f;
  }
  uVar5 = 0;
  do {
    bVar1 = PTR_DAT_0005724c[uVar5 * 0x10];
    uVar2 = (*(code *)PTR_FUN_00057250)(uVar5);
    cVar3 = FUN_000570ac(uVar5);
    if ((uVar2 & 4) == 4) {
      pbVar4 = local_54 + bVar1;
      *pbVar4 = *pbVar4 & 0xfe;
      *pbVar4 = *pbVar4 | 4;
      *pbVar4 = *pbVar4 | 8;
    }
    if ((uVar2 & 2) == 2) {
      pbVar4 = local_54 + bVar1;
      *pbVar4 = *pbVar4 & 0xfe;
      *pbVar4 = *pbVar4 | 2;
      *pbVar4 = *pbVar4 | 8;
    }
    uVar5 = uVar5 + 1;
    if (cVar3 == '\x01') {
      pbVar4 = local_54 + bVar1;
      *pbVar4 = *pbVar4 | 0x10;
    }
  } while (uVar5 < 0x49);
  (*(code *)PTR_FUN_00057238)(PTR_DAT_00057254,local_54,0x33);
  return;
}

