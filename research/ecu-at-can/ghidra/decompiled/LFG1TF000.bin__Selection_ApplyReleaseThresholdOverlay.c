/* Ghidra analysis output; verify against original SH instructions. */

/* Independent whole state/curve model:5531 direct,10 retained,36 selection replays;
   tcu-release-thresholds.txt. Active/release9B64; entry and exit not evaluated same call. Bounded
   fault replay can suppress creation; natural entry/task timing open. */

void Selection_ApplyReleaseThresholdOverlay(void)

{
  undefined *puVar1;
  undefined *puVar2;
  byte bVar3;
  byte bVar4;
  byte bVar5;
  char cVar6;
  byte bVar7;
  uint uVar8;
  
  bVar4 = CAN231_SixStateSource;
  bVar3 = TransmissionStateClass;
  puVar1 = PTR_Selection_ReleaseOverlayState_00045b94;
  bVar5 = *PTR_Selection_ReleaseOverlayState_00045b94 & 1;
  bVar7 = *(byte *)(int)DAT_00045b8e;
  uVar8 = -(((*PTR_Selection_ReleaseOverlayState_00045b94 & 2) == 0) - 1);
  if (bVar7 <= CAN231_SixStateSource) {
    *(undefined2 *)(int)DAT_00045b90 = DAT_ffff80ea;
  }
  cVar6 = Selection_AdmitReleaseThresholdOverlay();
  if (cVar6 == '\x01') {
    if (bVar5 == 0) {
      cVar6 = Selection_EnterReleaseThresholdOverlay();
      if (cVar6 != '\x01') goto LAB_00045b3c;
      bVar5 = 1;
    }
    else {
      cVar6 = Selection_ReleaseThresholdOverlay();
      puVar2 = PTR_Selection_ReleaseOverlayTimer_00045b98;
      if (cVar6 == '\x01') {
        if ((uVar8 & 0xff) == 0) {
          uVar8 = 1;
          *PTR_Selection_ReleaseOverlayTimer_00045b98 = 0;
        }
        if (((byte)*puVar2 <
             (byte)PTR_Selection_OverlayReleaseDurations_00045b9c[Selection_ApplicationIndex]) &&
           (bVar7 <= bVar4)) goto LAB_00045b3c;
        goto LAB_00045b38;
      }
    }
  }
  else {
LAB_00045b38:
    bVar5 = 0;
  }
  uVar8 = 0;
LAB_00045b3c:
  if (bVar5 == 0) {
    bVar7 = *puVar1 & 0xfe;
  }
  else {
    bVar7 = *puVar1 | 1;
  }
  *puVar1 = bVar7;
  if ((uVar8 & 0xff) == 0) {
    bVar7 = *puVar1 & 0xfd;
  }
  else {
    bVar7 = *puVar1 | 2;
  }
  *puVar1 = bVar7;
  Selection_UpdateOverlayMeasurementLatch(bVar5,uVar8);
  if (bVar5 == 1) {
    Selection_BuildReleaseThresholdCurves(uVar8);
  }
  *(byte *)(int)DAT_00045b8e = bVar4;
  *(byte *)(int)DAT_00045b92 = bVar3;
  return;
}

