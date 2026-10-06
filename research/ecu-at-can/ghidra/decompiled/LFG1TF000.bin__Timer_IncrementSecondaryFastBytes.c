/* Ghidra analysis output; verify against original SH instructions. */

/* Bytes82BC..82D0 end exclusive;8/16 secondary slots, executed. */

void Timer_IncrementSecondaryFastBytes(void)

{
  undefined *puVar1;
  uint uVar2;
  
  puVar1 = PTR_PTR_00011218;
  for (uVar2 = *(uint *)PTR_PTR_00011214; uVar2 < *(uint *)puVar1; uVar2 = uVar2 + 1) {
    Timer_IncrementByteUntilFF(uVar2);
  }
  return;
}

