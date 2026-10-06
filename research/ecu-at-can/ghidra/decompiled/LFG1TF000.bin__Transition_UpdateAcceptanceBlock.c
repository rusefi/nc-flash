/* Ghidra analysis output; verify against original SH instructions. */

/* 9545mask04 = (oldmask04 OR r4byte in0/5) AND (r4byte==954D OR r4byte==FF) AND (9594==2
   OR959C==2). Otherbits preserved;65536 matrix and3072 byte sweep cases. */

void Transition_UpdateAcceptanceBlock(uint param_1)

{
  int iVar1;
  char cVar2;
  char cVar3;
  byte bVar4;
  char cVar5;
  
  iVar1 = iRam0002d238;
  param_1 = param_1 & 0xff;
  cVar5 = -(((*(byte *)(iRam0002d238 + 1) & 4) == 0) + -1);
  if ((param_1 == 0) || (param_1 == 5)) {
    cVar5 = '\x01';
  }
  if (cVar5 == '\x01') {
    cVar2 = (*pcRam0002d23c)();
    cVar3 = (*pcRam0002d240)();
    if (((param_1 != *(byte *)(int)sRam0002d234) && (param_1 != (int)sRam0002d236)) ||
       ((cVar2 != '\x02' && (cVar3 != '\x02')))) {
      cVar5 = '\0';
    }
  }
  if (cVar5 == '\0') {
    bVar4 = *(byte *)(iVar1 + 1) & 0xfb;
  }
  else {
    bVar4 = *(byte *)(iVar1 + 1) | 4;
  }
  *(byte *)(iVar1 + 1) = bVar4;
  return;
}

