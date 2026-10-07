/* Ghidra analysis output; verify against original SH instructions. */

/* Second4530C producer. Prior-input hysteresis46580 precedes admission46372 and capture463CC.
   Retained low3 flags latch and replace slots1..3/6..8 operation6/kind5; source6 can publish
   despite rejected admission/no replacement.3906 direct cases,11 retained calls,24 full replays;
   tcu-retained-thresholds.txt. */

void Selection_ApplyRetainedThresholdOverlay(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined *puVar5;
  undefined *puVar6;
  char cVar7;
  char cVar8;
  char cVar9;
  byte bVar10;
  byte bVar11;
  byte *pbVar12;
  
  pbVar12 = (byte *)(int)DAT_000462ac;
  cVar8 = -(((*pbVar12 & 4) == 0) + -1);
  cVar9 = -(((*pbVar12 & 2) == 0) + -1);
  bVar10 = *pbVar12 & 1;
  Selection_UpdateOverlayHysteresis();
  cVar7 = Selection_AdmitRetainedThresholdOverlay();
  if ((cVar7 == '\x01') && (Selection_CaptureRetainedOverlayInputs(), (*pbVar12 & 8) != 0)) {
    if (cVar8 == '\0') {
      cVar8 = Selection_AdmitOverlayLatch(2);
    }
    if (cVar9 == '\0') {
      cVar9 = Selection_AdmitOverlayLatch(1);
    }
    if (bVar10 == 0) {
      bVar10 = Selection_AdmitOverlayLatch(0);
    }
    if (cVar8 == '\0') {
      bVar11 = *pbVar12 & 0xfb;
    }
    else {
      bVar11 = *pbVar12 | 4;
    }
    *pbVar12 = bVar11;
    if (cVar9 == '\0') {
      bVar11 = *pbVar12 & 0xfd;
    }
    else {
      bVar11 = *pbVar12 | 2;
    }
    *pbVar12 = bVar11;
    if (bVar10 == 0) {
      bVar11 = *pbVar12 & 0xfe;
    }
    else {
      bVar11 = *pbVar12 | 1;
    }
    *pbVar12 = bVar11;
    puVar6 = PTR_Selection_RetainedOverlayCurves_24__000463b4;
    puVar5 = PTR_Selection_RetainedOverlayCurves_000463b0;
    puVar4 = PTR_DAT_000463ac;
    puVar3 = PTR_Selection_ThresholdOperations_000463a8;
    puVar2 = PTR_DAT_000463a4;
    puVar1 = PTR_Selection_OverlayAppliedFlags_000463a0;
    if (((cVar8 == '\x01') || (cVar9 == '\x01')) || (bVar10 == 1)) {
      *PTR_Selection_OverlayAppliedFlags_000463a0 = *PTR_Selection_OverlayAppliedFlags_000463a0 | 4;
      *(undefined **)(puVar2 + 0xc) = puVar5;
      puVar3[3] = 6;
      puVar4[3] = 5;
      *(undefined **)(puVar2 + 0x20) = puVar6;
      puVar3[8] = 6;
      puVar4[8] = 5;
      if ((cVar9 == '\x01') || (bVar10 == 1)) {
        *puVar1 = *puVar1 | 2;
        *(undefined **)(puVar2 + 8) = PTR_Selection_RetainedOverlayCurves_48__000463b8;
        puVar3[2] = 6;
        puVar5 = PTR_Selection_RetainedOverlayCurves_72__000463bc;
        puVar4[2] = 5;
        *(undefined **)(puVar2 + 0x1c) = puVar5;
        puVar3[7] = 6;
        puVar4[7] = 5;
        if (bVar10 == 1) {
          *puVar1 = *puVar1 | 1;
          puVar1 = PTR_Selection_RetainedOverlayCurves_120__000463c4;
          *(undefined **)(puVar2 + 4) = PTR_Selection_RetainedOverlayCurves_96__000463c0;
          puVar3[1] = 6;
          puVar4[1] = 5;
          *(undefined **)(puVar2 + 0x18) = puVar1;
          puVar3[6] = 6;
          puVar4[6] = 5;
        }
      }
    }
  }
  if ((cVar7 != '\0') && ((*(byte *)(int)DAT_0004639e & 8) != 0)) {
    return;
  }
  Selection_ClearRetainedOverlayLatches();
  return;
}

