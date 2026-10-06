/* Ghidra analysis output; verify against original SH instructions. */

/* r0 value,r1=(MSB-offset<<8)|width,r2 destination byte. Verified576 cases. */

void Pack_MsbRelativeBitfield(void)

{
  byte in_r0;
  uint in_r1;
  byte *in_r2;
  uint uVar1;
  int iVar2;
  byte bVar3;
  byte bVar4;
  byte bVar5;
  
  bVar4 = 0;
  uVar1 = in_r1 & 0xff;
  bVar3 = 0xff;
  do {
    bVar5 = bVar3 << 1;
    bVar4 = bVar4 * '\x02' + 1;
    if ((int)(uVar1 - 1) < 1) break;
    bVar5 = bVar3 << 2;
    uVar1 = uVar1 - 2;
    bVar4 = bVar4 * '\x02' + 1;
    bVar3 = bVar5;
  } while (0 < (int)uVar1);
  bVar4 = in_r0 & bVar4;
  iVar2 = (8 - (in_r1 & 0xff)) - ((in_r1 & 0xff00) >> 8);
  bVar3 = bVar4;
  if (iVar2 != 0) {
    do {
      bVar4 = bVar3 << 1;
      bVar5 = bVar5 * '\x02' + 1;
      if (iVar2 + -1 < 1) break;
      bVar4 = bVar3 << 2;
      iVar2 = iVar2 + -2;
      bVar5 = bVar5 * '\x02' + 1;
      bVar3 = bVar4;
    } while (0 < iVar2);
  }
  *in_r2 = bVar4 | bVar5 & *in_r2;
  return;
}

