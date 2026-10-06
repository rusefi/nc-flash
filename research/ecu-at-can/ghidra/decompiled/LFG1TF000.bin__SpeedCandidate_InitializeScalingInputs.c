/* Ghidra analysis output; verify against original SH instructions. */

/* Static: initializesA550/A552 from ROM5FD7C=196; physical meaning unverified. */

void SpeedCandidate_InitializeScalingInputs(void)

{
  undefined2 *puVar1;
  
  puVar1 = puRam00051bf8;
  *(undefined2 *)PTR_DAT_00051bfc = *puRam00051bf8;
  *(undefined2 *)PTR_SpeedCandidate_ScalingInput_00051c00 = *puVar1;
  *PTR_DAT_00051c04 = 0;
  *PTR_DAT_00051c08 = 0;
  return;
}

