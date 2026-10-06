/* Ghidra analysis output; verify against original SH instructions. */

/* SR critical section fills24 signed32 words9248 with214B6()=73728;resets800D=0. After staleness,
   recovery gradually replaces defaults. See tcu-measurement.txt. */

void Measurement_ResetHistory(void)

{
  undefined4 uVar1;
  undefined4 uVar2;
  undefined4 *puVar3;
  int iVar4;
  
  uVar1 = Measurement_ReadResetPeriod();
  uVar2 = (*(code *)PTR_FUN_000214dc)();
  puVar3 = (undefined4 *)PTR_Measurement_CaptureHistory_000214e0;
  for (iVar4 = 0; iVar4 < (int)(uint)(byte)*PTR_DAT_000214e4; iVar4 = iVar4 + 1) {
    *puVar3 = uVar1;
    puVar3 = puVar3 + 1;
  }
  Measurement_HistoryHead = 0;
  (*(code *)PTR_FUN_000214e8)(uVar2);
  return;
}

