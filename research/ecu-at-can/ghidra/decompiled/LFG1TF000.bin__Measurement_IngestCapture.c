/* Ghidra analysis output; verify against original SH instructions. */

/* 8908 capped73728; old810C>=130 forces cap. Advances800D modulo24, stores9248[head],
   saturates800C, savesoldage9244, clears810C.540 raw boundary cases; negative synthetic inputs
   survive upper-only caps. See tcu-measurement.txt. */

void Measurement_IngestCapture(void)

{
  byte bVar1;
  undefined *UNRECOVERED_JUMPTABLE;
  undefined *puVar2;
  
  bVar1 = *PTR_Measurement_CurrentCaptureAge_000212b0;
  if ((DAT_000212ac <= (short)(ushort)bVar1) ||
     (puVar2 = *(undefined **)PTR_Measurement_CaptureDeltaDiv10_000212bc,
     (int)PTR_DAT_000212c0 < (int)*(undefined **)PTR_Measurement_CaptureDeltaDiv10_000212bc)) {
    puVar2 = PTR_DAT_000212c0;
  }
  UNRECOVERED_JUMPTABLE = (undefined *)Measurement_ReadResetPeriod();
  if ((int)UNRECOVERED_JUMPTABLE < (int)puVar2) {
    puVar2 = UNRECOVERED_JUMPTABLE;
  }
  Measurement_HistoryHead = Measurement_HistoryHead + 1;
  if ((byte)*PTR_DAT_000212c4 <= Measurement_HistoryHead) {
    Measurement_HistoryHead = 0;
  }
  *(undefined **)(PTR_Measurement_CaptureHistory_000212c8 + (uint)Measurement_HistoryHead * 4) =
       puVar2;
  UNRECOVERED_JUMPTABLE = PTR_LAB_000212cc;
  if ((short)(ushort)Measurement_CaptureCount < DAT_000212a8) {
    Measurement_CaptureCount = Measurement_CaptureCount + 1;
  }
  *(byte *)(int)DAT_000212aa = bVar1;
  *PTR_Measurement_CurrentCaptureAge_000212b0 = 0;
                    /* WARNING: Could not recover jumptable at 0x00021248. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*(code *)UNRECOVERED_JUMPTABLE)(puVar2);
  return;
}

