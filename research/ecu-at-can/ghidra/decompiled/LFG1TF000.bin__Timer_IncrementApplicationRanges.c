/* Ghidra analysis output; verify against original SH instructions. */

/* Bytes8188..8281 and words8330..8372 end exclusive; includes81EB/822C/D/F and hold
   timers81F2..81FD.2/16 primary slots; fullrange guardchecks and retained49B08 observations in
   tcu-adjustment-timers.txt. Physical period open. */

void Timer_IncrementApplicationRanges(void)

{
  undefined *puVar1;
  undefined *puVar2;
  uint uVar3;
  
  puVar1 = PTR_PTR_0001111c;
  for (uVar3 = *(uint *)PTR_PTR_00011118; puVar2 = PTR_PTR_00011124, uVar3 < *(uint *)puVar1;
      uVar3 = uVar3 + 1) {
    Timer_IncrementByteUntilFF(uVar3);
  }
  for (uVar3 = *(uint *)PTR_PTR_00011120; uVar3 < *(uint *)puVar2; uVar3 = uVar3 + 2) {
    Timer_IncrementWordUntilFFFF(uVar3);
  }
  return;
}

