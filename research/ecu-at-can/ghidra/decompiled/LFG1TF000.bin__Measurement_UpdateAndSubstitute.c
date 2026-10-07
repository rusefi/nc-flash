/* Ghidra analysis output; verify against original SH instructions. */

/* 212F4(ROM76DE2=360)->80EE; normal9234=measurement;92C6bit4 orAC86 selects9218[index],
   uppercap32767, no lowercap.8080FF index6 else8081.9236 retainsmeasurement; tail50D88 executes.392
   substitution cases. See tcu-measurement.txt. Full126EC capture/frame experiment verifies
   everycall measurement/period from independent24-slot timestamp history; firstcall stale reset.
   See tcu-captured-requests.txt. */

void Measurement_UpdateAndSubstitute(void)

{
  undefined *puVar1;
  undefined2 uVar2;
  byte bVar4;
  int iVar3;
  
  Phase_MeasuredSourceSample = Measurement_CalculateFromHistory((int)*(short *)PTR_DAT_000212d0);
  if (((*PTR_ApplicationFaultFlags92C6_000212d8 & 0x10) == 0) && (*PTR_DAT_000212dc == '\0')) {
    *(undefined2 *)PTR_Measurement_SelectedInternalSample_000212d4 = Phase_MeasuredSourceSample;
  }
  else {
    bVar4 = CAN231_SixStateSource;
    if (TransmissionStateClass == 0xff) {
      bVar4 = 6;
    }
    iVar3 = *(int *)(PTR_Phase_ProducedReferenceWords_000212e0 + (uint)bVar4 * 4);
    if ((int)DAT_000212ae < *(int *)(PTR_Phase_ProducedReferenceWords_000212e0 + (uint)bVar4 * 4)) {
      iVar3 = (int)DAT_000212ae;
    }
    *(short *)PTR_Measurement_SelectedInternalSample_000212d4 = (short)iVar3;
  }
  uVar2 = (*(code *)PTR_FUN_000212e4)();
  puVar1 = PTR_FUN_000212ec;
  *(undefined2 *)PTR_Measurement_UnsubstitutedCopy_000212e8 = uVar2;
  (*(code *)puVar1)();
  (*(code *)PTR_FUN_000212f0)();
  return;
}

