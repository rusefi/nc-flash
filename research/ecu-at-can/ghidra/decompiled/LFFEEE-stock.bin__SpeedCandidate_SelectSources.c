/* Ghidra analysis output; verify against original SH instructions. */

/* Decode4B0 words via binary32 0.01,-100; average/select valid input under7353; else MTcached6D64
   or AT216-derived6E18. 8EC6=1 ->65537. Physical units unproven. */

undefined4 * SpeedCandidate_SelectSources(void)

{
  char cVar1;
  char cVar2;
  char cVar3;
  undefined4 *puVar4;
  float fVar5;
  float fVar6;
  undefined4 uVar7;
  undefined4 uVar8;
  
  cVar1 = *PTR_CAN4B0_SelectionEnabled_0003a21c;
  cVar2 = *PTR_CAN4B0_Word6Invalid_0003a220;
  cVar3 = *PTR_CAN4B0_Word4Invalid_0003a224;
  uVar7 = DAT_0003a228;
  uVar8 = DAT_0003a22c;
  fVar5 = (float)(*(code *)PTR_FUN_0003a234)
                           (DAT_0003a228,DAT_0003a22c,
                            (int)*(short *)PTR_CAN4B0_WorkingWord4_0003a230);
  fVar6 = (float)(*(code *)PTR_FUN_0003a234)
                           (uVar7,uVar8,(int)*(short *)PTR_CAN4B0_WorkingWord6_0003a238);
  if (fVar5 < 0.0) {
    fVar5 = 0.0;
  }
  if (fVar6 < 0.0) {
    fVar6 = 0.0;
  }
  uVar7 = (*(code *)PTR_FUN_0003a23c)();
  *(undefined4 *)PTR_SpeedCandidate_CachedFallback_0003a240 = uVar7;
  if (*PTR_DAT_0003a248 == '\x01') {
    *(undefined4 *)PTR_SpeedCandidate_Selected_0003a244 = DAT_0003a24c;
    return &DAT_0003a24c;
  }
  if (cVar1 == '\x01') {
    if ((cVar2 != '\x01') || (puVar4 = (undefined4 *)0x0, cVar3 != '\0')) {
      if ((cVar3 == '\x01') && (cVar2 == '\0')) {
        *(float *)PTR_SpeedCandidate_Selected_0003a244 = fVar6;
        return (undefined4 *)0x1;
      }
      if ((cVar3 != '\0') || (cVar2 != '\0')) goto LAB_0003a130;
      fVar5 = (fVar5 + fVar6) / 2.0;
      puVar4 = (undefined4 *)0x1;
    }
    *(float *)PTR_SpeedCandidate_Selected_0003a244 = fVar5;
  }
  else {
LAB_0003a130:
    puVar4 = (undefined4 *)(int)(char)*PTR_TransmissionModeFlags_0003a250;
    if (((uint)puVar4 & 0x40) == 0) {
      uVar7 = *(undefined4 *)PTR_CAN216_SpeedCandidateFallback_0003a254;
    }
    else {
      uVar7 = *(undefined4 *)PTR_SpeedCandidate_CachedFallback_0003a240;
    }
    *(undefined4 *)PTR_SpeedCandidate_Selected_0003a244 = uVar7;
  }
  return puVar4;
}

