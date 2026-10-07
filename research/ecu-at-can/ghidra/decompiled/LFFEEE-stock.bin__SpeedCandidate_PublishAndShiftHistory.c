/* Ghidra analysis output; verify against original SH instructions. */

/* 6D58 passes to protected6D5C unless8EC6 exact1 or value>65536 thenzero.
   Protected6D68=RTZ(RTZ(abs(RTZ(old6D88-new))*20)/3); shift six raw floats6D74..6D88 and
   insertnew.6912 cases/all flag bytes and320 retained chains; no acceleration-unit claim. */

void SpeedCandidate_PublishAndShiftHistory(void)

{
  undefined *puVar1;
  undefined4 *puVar2;
  char cVar3;
  undefined4 *puVar4;
  float fVar5;
  float fVar6;
  
  fVar6 = *(float *)PTR_SpeedCandidate_Selected_0003a244;
  if ((*PTR_DAT_0003a248 == '\x01') || (DAT_0003a258 < fVar6)) {
    fVar6 = 0.0;
  }
  (*(code *)PTR_FUN_0003a214)(fVar6,PTR_SpeedCandidate_ProtectedSelected_0003a210);
  puVar1 = PTR_SpeedCandidate_SixSampleHistory_0003a25c;
  fVar5 = (float)(*(code *)PTR_FUN_0003a260)
                           (*(undefined4 *)(PTR_SpeedCandidate_SixSampleHistory_0003a25c + 0x14),
                            fVar6);
  (*(code *)PTR_FUN_0003a214)
            ((fVar5 * DAT_0003a264) / DAT_0003a268,PTR_SpeedCandidate_HistoryDifference_0003a218);
  cVar3 = '\x05';
  puVar2 = (undefined4 *)(puVar1 + 0x10);
  puVar4 = (undefined4 *)(puVar1 + 0x18);
  do {
    cVar3 = cVar3 + -1;
    puVar4 = puVar4 + -1;
    *puVar4 = *puVar2;
    puVar2 = puVar2 + -1;
  } while (cVar3 != '\0');
  *(float *)puVar1 = fVar6;
  return;
}

