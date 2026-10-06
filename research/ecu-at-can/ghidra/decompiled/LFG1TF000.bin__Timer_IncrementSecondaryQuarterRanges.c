/* Ghidra analysis output; verify against original SH instructions. */

/* Bytes82D0..82DC and word8374;4/16 secondary slots, executed. */

void Timer_IncrementSecondaryQuarterRanges(void)

{
  undefined *puVar1;
  undefined *puVar2;
  uint uVar3;
  
  puVar1 = PTR_PTR_00011220;
  for (uVar3 = *(uint *)PTR_PTR_0001121c; puVar2 = PTR_PTR_00011228, uVar3 < *(uint *)puVar1;
      uVar3 = uVar3 + 1) {
    Timer_IncrementByteUntilFF(uVar3);
  }
  for (uVar3 = *(uint *)PTR_PTR_00011224; uVar3 < *(uint *)puVar2; uVar3 = uVar3 + 2) {
    Timer_IncrementWordUntilFFFF(uVar3);
  }
  return;
}

