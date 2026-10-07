/* Ghidra analysis output; verify against original SH instructions. */

/* 6927 decrements if67D4>16.973400115966797,67D0<10.9375,91E5!=1,raw9462!=1; else
   reload200.1600cases/240retained; separate19E12caller, nohardwareperiod. */

void ControlMode_ExpiryCounter(void)

{
  undefined *puVar1;
  char cVar2;
  
  puVar1 = PTR_ControlMode_ExpiryCountdown_00030820;
  if ((((*(float *)PTR_ControlMode_ScaledByteInput_00030828 <= *(float *)PTR_DAT_00030824) ||
       (*(float *)PTR_DAT_0003082c <= *(float *)PTR_ControlMode_BiasedInput_00030830)) ||
      (*PTR_Control_ActivityHoldFlag_00030834 == '\x01')) ||
     (cVar2 = (*(code *)PTR_FUN_0003083c)(PTR_DAT_00030838), cVar2 == '\x01')) {
    *puVar1 = *PTR_DAT_00030840;
  }
  else if (*puVar1 != '\0') {
    *puVar1 = *puVar1 + (char)DAT_00030818;
  }
  return;
}

