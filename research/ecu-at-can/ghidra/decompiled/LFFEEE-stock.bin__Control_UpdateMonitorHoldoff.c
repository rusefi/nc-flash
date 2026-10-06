/* Ghidra analysis output; verify against original SH instructions. */

/* 5680reload125when536C<6and6600==1;otherwise decrementnonzero.
   Equality6doesnotreload.126callreload/countdown verified. */

void Control_UpdateMonitorHoldoff(void)

{
  if ((*(float *)PTR_DAT_00024f40 <= *(float *)PTR_Control_FilteredLocalSource_00024f44) ||
     (*PTR_DAT_00024f48 != '\x01')) {
    if (*(short *)PTR_Control_SerialMonitorHoldoffCounter_00024f3c != 0) {
      *(short *)PTR_Control_SerialMonitorHoldoffCounter_00024f3c =
           *(short *)PTR_Control_SerialMonitorHoldoffCounter_00024f3c + (short)DAT_00024f50;
    }
  }
  else {
    *(undefined2 *)PTR_Control_SerialMonitorHoldoffCounter_00024f3c =
         *(undefined2 *)PTR_DAT_00024f4c;
  }
  return;
}

