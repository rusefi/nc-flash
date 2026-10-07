/* Ghidra analysis output; verify against original SH instructions. */

/* Calls6CD96, reloads8EF4/5=50,8EF6/7=3, tailcalls6CF06.20 wrapper checks. See
   control-raw-enable.txt. */

void Control_InitFirstRawQualification(void)

{
  undefined *puVar1;
  undefined *puVar2;
  
  Control_QualifyRawChannel28();
  puVar2 = PTR_DAT_0006ce70;
  puVar1 = PTR_DAT_0006ce68;
  *PTR_DAT_0006ce6c = *PTR_DAT_0006ce68;
  *puVar2 = *puVar1;
  puVar1 = PTR_DAT_0006ce74;
  *PTR_DAT_0006ce78 = *PTR_DAT_0006ce74;
  *PTR_DAT_0006ce7c = *puVar1;
  Control_UpdateFirstRawFallbackLatches();
  return;
}

