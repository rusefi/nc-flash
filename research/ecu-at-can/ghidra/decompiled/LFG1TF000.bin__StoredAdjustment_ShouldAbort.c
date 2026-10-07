/* Ghidra analysis output; verify against original SH instructions. */

/* Accepted change or previouspending/currentnotpending plus group timer>=stock183.720 cases;
   retained timer runs show disappearance below183 loses pendinghistory, laterthreshold alone
   doesnotabort. Actual cadence/reachability unproved. */

undefined4 StoredAdjustment_ShouldAbort(void)

{
  ushort uVar1;
  char cVar2;
  byte bVar3;
  uint uVar4;
  undefined4 uVar5;
  
  uVar1 = *(ushort *)(int)DAT_00049fb4;
  cVar2 = (*(code *)PTR_Phase_HasPendingWork_00049fc0)();
  uVar4 = 0;
  if (uVar1 < 3) {
    uVar4 = (*(code *)PTR_ApplicationCode_SelectThresholdFamily_00049fc4)((int)(short)uVar1);
  }
  if (uVar1 == 0) {
    bVar3 = *PTR_StoredAdjustment_Group0AbortTimer_00049fc8;
  }
  else if (uVar1 == 1) {
    bVar3 = *PTR_StoredAdjustment_Group1AbortTimer_00049fcc;
  }
  else {
    bVar3 = *PTR_StoredAdjustment_Group2AbortTimer_00049fd0;
  }
  uVar5 = 0;
  if ((((*(char *)(int)DAT_00049fb6 != '\0') && (cVar2 == '\0')) &&
      ((byte)PTR_DAT_00049fd4[(uint)DAT_ffff808d + (uVar4 & 0xff) * 6] <= bVar3)) ||
     (CAN231_SixStateSource != *(byte *)(int)DAT_00049fb8)) {
    uVar5 = 1;
  }
  return uVar5;
}

