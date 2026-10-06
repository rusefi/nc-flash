/* Ghidra analysis output; verify against original SH instructions. */

/* Saturating byte interval810C..8157 end exclusive; includes twelve request ramp
   timers8115..8120;8/16 primary slots. */

void Timer_IncrementFastBytes(void)

{
  undefined *puVar1;
  uint uVar2;
  
  puVar1 = PTR_PTR_000110fc;
  for (uVar2 = *(uint *)PTR_Timer_RangeBoundaryPointers_000110f8; uVar2 < *(uint *)puVar1;
      uVar2 = uVar2 + 1) {
    Timer_IncrementByteUntilFF(uVar2);
  }
  return;
}

