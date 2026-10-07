/* Ghidra analysis output; verify against original SH instructions. */

/* Returns1 unless class8080 isFF/0/1/2 or9330bit0 set.1024 original cases include all256 class
   bytes; unusual values are helper coverage, not physical valid states. */

undefined4 Selection_AdmitRetainedThresholdOverlay(void)

{
  undefined4 uVar1;
  
  uVar1 = 0;
  if ((((TransmissionStateClass != 0xff) && (TransmissionStateClass != 0)) &&
      (TransmissionStateClass != 2)) &&
     ((TransmissionStateClass != 1 && ((*PTR_DAT_000463c8 & 1) == 0)))) {
    uVar1 = 1;
  }
  return uVar1;
}

