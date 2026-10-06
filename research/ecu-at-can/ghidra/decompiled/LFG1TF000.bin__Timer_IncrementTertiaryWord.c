/* Ghidra analysis output; verify against original SH instructions. */

/* Increments word837C once per512 primary calls from reset; executed. */

void Timer_IncrementTertiaryWord(void)

{
  undefined *puVar1;
  uint uVar2;
  
  puVar1 = PTR_PTR_000112c4;
  for (uVar2 = *(uint *)PTR_PTR_000112c0; uVar2 < *(uint *)puVar1; uVar2 = uVar2 + 2) {
    Timer_IncrementWordUntilFFFF(uVar2);
  }
  return;
}

