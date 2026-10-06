/* Ghidra analysis output; verify against original SH instructions. */

/* Byte82DC and words8378,837A; secondary phase7, executed. */

void Timer_IncrementSecondarySlowRanges(void)

{
  undefined *puVar1;
  undefined *puVar2;
  uint uVar3;
  
  puVar1 = PTR_PTR_00011230;
  for (uVar3 = *(uint *)PTR_PTR_0001122c; puVar2 = PTR_PTR_00011238, uVar3 < *(uint *)puVar1;
      uVar3 = uVar3 + 1) {
    Timer_IncrementByteUntilFF(uVar3);
  }
  for (uVar3 = *(uint *)PTR_PTR_00011234; uVar3 < *(uint *)puVar2; uVar3 = uVar3 + 2) {
    Timer_IncrementWordUntilFFFF(uVar3);
  }
  return;
}

