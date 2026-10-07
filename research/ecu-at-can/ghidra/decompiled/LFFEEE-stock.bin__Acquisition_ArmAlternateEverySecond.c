/* Ghidra analysis output; verify against original SH instructions. */

/* 40A2 byte increment/wrap then >=2 reset; zero captures11/23 initial samples, updates40A0
   threshold1000/1050 hysteresis, calls531E(0),5D62(mode), clears40A1. Executed all256 counters and
   boundary/retained flags. */

void Acquisition_ArmAlternateEverySecond(void)

{
  undefined *puVar1;
  undefined2 *puVar2;
  
  puVar1 = PTR_Acquisition_AlternateHalfCounter_00005dac;
  *PTR_Acquisition_AlternateHalfCounter_00005dac =
       *PTR_Acquisition_AlternateHalfCounter_00005dac + '\x01';
  if (1 < (byte)*puVar1) {
    *puVar1 = 0;
  }
  if (*puVar1 == '\0') {
    puVar2 = (undefined2 *)(int)DAT_00005d8c;
    *(undefined2 *)PTR_Acquisition_AlternateInitialSample23_00005db0 = *puVar2;
    *(undefined2 *)PTR_DAT_00005db4 = puVar2[-0x10];
    if (*(float *)PTR_DAT_00005dbc < *(float *)PTR_DAT_00005db8) {
      if (*(float *)PTR_DAT_00005dbc + *(float *)PTR_DAT_00005dc4 < *(float *)PTR_DAT_00005db8) {
        *PTR_Acquisition_AlternateTimingMode_00005dc0 = 0;
      }
    }
    else {
      *PTR_Acquisition_AlternateTimingMode_00005dc0 = 1;
    }
    (*(code *)PTR_Acquisition_ArmExternalTrigger_00005dc8)(0);
    Acquisition_ConfigureAlternateTimers((int)(char)*PTR_Acquisition_AlternateTimingMode_00005dc0);
    *PTR_Acquisition_AlternateCaptureInhibit_00005dcc = 0;
  }
  return;
}

