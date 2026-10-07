/* Ghidra analysis output; verify against original SH instructions. */

/* 404B nonzero executes5E38 then clears marker even if capture inhibited; otherwise4049 exact1
   calls5CF4. Full original code verified; software marker is not hardware ADF. See
   control-acquisition-completion.txt. */

uint Acquisition_FollowCompletion(void)

{
  uint uVar1;
  
  if (*PTR_Acquisition_AlternateArmed_00004ecc == '\0') {
    uVar1 = (uint)(byte)*PTR_Acquisition_ExtendedBankFlag_00004ed4;
    if (uVar1 == 1) {
      uVar1 = (*(code *)PTR_Acquisition_ArmAlternateEverySecond_00004ed8)();
      return uVar1;
    }
  }
  else {
    uVar1 = (*DAT_00004edc)();
    *PTR_Acquisition_AlternateArmed_00004ecc = 0;
  }
  return uVar1;
}

