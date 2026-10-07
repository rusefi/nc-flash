/* Ghidra analysis output; verify against original SH instructions. */

/* Newpendingqueue,group0..2,eventmaskclear,proposed=accepted,transitionbitclear,81EB>=122,9B3D0/1.1080
   cases. Pending observedtooearly needsfresh edgeaftertimerqualification; retained originaltimer
   proof in tcu-adjustment-timers.txt. */

undefined4 StoredAdjustment_AdmitCapture(void)

{
  bool bVar1;
  char cVar2;
  char cVar3;
  int iVar4;
  undefined4 uVar5;
  byte *pbVar6;
  
  cVar2 = DAT_ffff8089;
  cVar3 = (*(code *)PTR_Phase_HasPendingWork_00049ed0)();
  uVar5 = 0;
  iVar4 = 0;
  bVar1 = false;
  if ((cVar3 != '\0') && (*(char *)(int)DAT_00049ec8 == '\0')) {
    pbVar6 = (byte *)(int)DAT_00049eca;
    if (cVar2 == '\0') {
      if ((*pbVar6 & 0x10) == 0) {
        bVar1 = true;
        iVar4 = 0;
      }
    }
    else if (cVar2 == '\x01') {
      if ((*pbVar6 & 0x20) == 0) {
        bVar1 = true;
        iVar4 = 1;
      }
    }
    else if ((cVar2 == '\x02') && ((*pbVar6 & 0x40) == 0)) {
      bVar1 = true;
      iVar4 = 2;
    }
  }
  if ((((bVar1) && (*(byte *)(int)DAT_00049ecc == CAN231_SixStateSource)) &&
      (((int)*(char *)(int)DAT_00049eca & 0x80U) == 0)) &&
     (((byte)PTR_DAT_00049edc[iVar4] <=
       (byte)*PTR_StoredAdjustment_CaptureQualificationTimer_00049ed8 &&
      ((*PTR_DAT_00049ed4 == '\0' || (*PTR_DAT_00049ed4 == '\x01')))))) {
    uVar5 = 1;
  }
  return uVar5;
}

