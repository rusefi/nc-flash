/* Ghidra analysis output; verify against original SH instructions. */

/* 72FC>.5 clears7344;<=.25 sets1;deadband retains even nonBoolean history. Executed originalbody.
    */

void Control_UpdateSelectedValueHysteresis(void)

{
  if (*(float *)PTR_Control_SelectedPublishedValue_000426e0 <= *(float *)PTR_DAT_000426e4) {
    if (*(float *)PTR_Control_SelectedPublishedValue_000426e0 <=
        *(float *)PTR_DAT_000426e4 - *(float *)PTR_DAT_000426e8) {
      *PTR_DAT_000426c8 = 1;
    }
  }
  else {
    *PTR_DAT_000426c8 = 0;
  }
  return;
}

