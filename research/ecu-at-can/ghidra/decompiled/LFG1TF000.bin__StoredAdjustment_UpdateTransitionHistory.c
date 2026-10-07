/* Ghidra analysis output; verify against original SH instructions. */

/* Retained9CA4bit7 set onpendingqueue/proposed!=accepted; clear when
   proposed=accepted=previousaccepted.162 cases. */

void StoredAdjustment_UpdateTransitionHistory(void)

{
  byte bVar1;
  char cVar2;
  byte bVar3;
  byte *pbVar4;
  char cVar5;
  
  bVar1 = Selection_ApplicationIndex;
  bVar3 = CAN231_SixStateSource;
  pbVar4 = (byte *)(int)DAT_00049dea;
  cVar5 = -((((int)(char)*pbVar4 & 0x80U) == 0) + -1);
  cVar2 = (*(code *)PTR_Phase_HasPendingWork_00049df0)();
  if ((cVar2 != '\0') && (bVar1 != bVar3)) {
    cVar5 = '\x01';
  }
  if ((bVar3 == bVar1) && (bVar3 == *(byte *)(int)DAT_00049dec)) {
    cVar5 = '\0';
  }
  if (cVar5 == '\0') {
    bVar3 = *pbVar4 & 0x7f;
  }
  else {
    bVar3 = *pbVar4 | 0x80;
  }
  *pbVar4 = bVar3;
  return;
}

