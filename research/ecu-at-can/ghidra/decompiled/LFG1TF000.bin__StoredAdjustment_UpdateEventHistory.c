/* Ghidra analysis output; verify against original SH instructions. */

/* Refresh9CA4 bits4/5/6 only when8084 rises vs9CA3; track9BFCbit0,9C00bit0 and
   composite9ACD/9C00.4096 cases. */

void StoredAdjustment_UpdateEventHistory(void)

{
  byte bVar1;
  bool bVar2;
  byte bVar3;
  byte bVar4;
  byte bVar5;
  byte *pbVar6;
  
  bVar3 = Selection_ApplicationIndex;
  bVar5 = *PTR_DAT_00049cf4;
  bVar1 = *PTR_DAT_00049cf8;
  bVar2 = false;
  if ((((*PTR_DAT_00049cfc & 0x10) != 0) || ((*PTR_DAT_00049cf8 & 0x10) != 0)) ||
     ((*PTR_DAT_00049cf8 & 2) == 0)) {
    bVar2 = true;
  }
  pbVar6 = (byte *)(int)DAT_00049cf0;
  if (*(byte *)(int)DAT_00049cf2 < Selection_ApplicationIndex) {
    if (((bVar5 & 1) == 1) && ((*(byte *)(int)DAT_00049cf0 & 2) == 0)) {
      bVar4 = *pbVar6 | 0x10;
    }
    else {
      bVar4 = *pbVar6 & 0xef;
    }
    *pbVar6 = bVar4;
    if (((bVar1 & 1) == 1) && ((*(byte *)(int)DAT_00049cf0 & 4) == 0)) {
      bVar4 = *pbVar6 | 0x20;
    }
    else {
      bVar4 = *pbVar6 & 0xdf;
    }
    *pbVar6 = bVar4;
    if ((bVar2) || ((*(byte *)(int)DAT_00049cf0 & 8) == 0)) {
      bVar4 = *pbVar6 & 0xbf;
    }
    else {
      bVar4 = *pbVar6 | 0x40;
    }
    *pbVar6 = bVar4;
  }
  *(byte *)(int)DAT_00049cf2 = bVar3;
  if ((bVar5 & 1) == 0) {
    bVar5 = *pbVar6 & 0xfd;
  }
  else {
    bVar5 = *pbVar6 | 2;
  }
  *pbVar6 = bVar5;
  if ((bVar1 & 1) == 0) {
    bVar5 = *pbVar6 & 0xfb;
  }
  else {
    bVar5 = *pbVar6 | 4;
  }
  *pbVar6 = bVar5;
  if (bVar2) {
    bVar5 = *pbVar6 | 8;
  }
  else {
    bVar5 = *pbVar6 & 0xf7;
  }
  *pbVar6 = bVar5;
  return;
}

