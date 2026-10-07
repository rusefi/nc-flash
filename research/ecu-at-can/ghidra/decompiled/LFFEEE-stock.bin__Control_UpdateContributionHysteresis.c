/* Ghidra analysis output; verify against original SH instructions. */

/* 812A clearsbelow69,setsabove75;equalboundsandintervalholdrawoldbyte.20boundarycases. */

void Control_UpdateContributionHysteresis(void)

{
  if (*(float *)PTR_DAT_0005988c - *(float *)PTR_DAT_00059890 <=
      *(float *)PTR_Control_FilteredContributionInput_0005987c) {
    if (*(float *)PTR_DAT_0005988c < *(float *)PTR_Control_FilteredContributionInput_0005987c) {
      *PTR_Control_FirstContributionHysteresis_00059888 = 1;
    }
  }
  else {
    *PTR_Control_FirstContributionHysteresis_00059888 = 0;
  }
  return;
}

