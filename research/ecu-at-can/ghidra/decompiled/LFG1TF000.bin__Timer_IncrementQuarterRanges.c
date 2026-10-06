/* Ghidra analysis output; verify against original SH instructions. */

/* Bytes8158..8188; signed-word8380..8410 and unsigned-word82E0..8330;4/16 primary slots, executed.
    */

void Timer_IncrementQuarterRanges(void)

{
  undefined *puVar1;
  undefined *puVar2;
  uint uVar3;
  
  puVar1 = PTR_PTR_00011104;
  for (uVar3 = *(uint *)PTR_PTR_00011100; puVar2 = PTR_PTR_0001110c, uVar3 < *(uint *)puVar1;
      uVar3 = uVar3 + 1) {
    Timer_IncrementByteUntilFF(uVar3);
  }
  for (uVar3 = *(uint *)PTR_PTR_00011108; puVar1 = PTR_PTR_00011114, uVar3 < *(uint *)puVar2;
      uVar3 = uVar3 + 2) {
    Timer_IncrementWordUntil7FFF(uVar3);
  }
  for (uVar3 = *(uint *)PTR_PTR_00011110; uVar3 < *(uint *)puVar1; uVar3 = uVar3 + 2) {
    Timer_IncrementWordUntilFFFF(uVar3);
  }
  return;
}

