/* Ghidra analysis output; verify against original SH instructions. */

/* Executed finite6CB0: >=stock10 sets91E6=1; <stock9 clears; [9,10) holds arbitrary oldbyte.
   2304cases and2 actual18DC8 boundaries. control-task.txt. */

void Control_UpdateActivityHysteresis(void)

{
  if (*(float *)PTR_Acquisition_FilteredInputCopy_00077fa4 < *(float *)PTR_DAT_00077fa8) {
    if (*(float *)PTR_Acquisition_FilteredInputCopy_00077fa4 <
        *(float *)PTR_DAT_00077fa8 - *(float *)PTR_DAT_00077fac) {
      *PTR_Control_ActivityHysteresisFlag_00077f9c = 0;
    }
  }
  else {
    *PTR_Control_ActivityHysteresisFlag_00077f9c = 1;
  }
  return;
}

