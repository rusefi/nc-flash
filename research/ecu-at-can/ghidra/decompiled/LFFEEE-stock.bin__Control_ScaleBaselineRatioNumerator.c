/* Ghidra analysis output; verify against original SH instructions. */

/* 8034 from80BC*7020 withsameorderedscalesas583EE. Upstream80BC/7020 producersremainopen. */

void Control_ScaleBaselineRatioNumerator(void)

{
  *(float *)PTR_Control_BaselineRatioNumerator_00058584 =
       (((*(float *)PTR_DAT_000585b8 * *DAT_000585b4) / DAT_000585a8) * *(float *)PTR_DAT_000585ac *
       *(float *)PTR_DAT_000585b0) / 2.0;
  return;
}

