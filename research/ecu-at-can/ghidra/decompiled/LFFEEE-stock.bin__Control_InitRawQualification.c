/* Ghidra analysis output; verify against original SH instructions. */

/* Calls6D876, resets counters8F2C/D=50 and8F2E/F=3, tailcalls6D9E6.16 whole-wrapper cases. See
   control-raw-provenance.txt. */

void Control_InitRawQualification(void)

{
  undefined *puVar1;
  undefined *puVar2;
  
  Control_QualifyRawChannel29();
  puVar2 = PTR_DAT_0006d950;
  puVar1 = PTR_DAT_0006d948;
  *PTR_DAT_0006d94c = *PTR_DAT_0006d948;
  *puVar2 = *puVar1;
  puVar1 = PTR_DAT_0006d954;
  *PTR_DAT_0006d958 = *PTR_DAT_0006d954;
  *PTR_DAT_0006d95c = *puVar1;
  Control_UpdateRawFallbackLatches();
  return;
}

