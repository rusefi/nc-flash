/* Ghidra analysis output; verify against original SH instructions. */

/* Original protected6D30=0. Three nonzero SR masks verified; see control-raw-inputs.txt. */

void Control_InitializeRawSnapshot(void)

{
  (*(code *)PTR_FUN_00039f10)(0,PTR_Control_RawFirstSnapshot_00039f0c);
  return;
}

