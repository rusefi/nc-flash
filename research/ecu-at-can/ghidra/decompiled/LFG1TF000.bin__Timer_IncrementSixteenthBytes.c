/* Ghidra analysis output; verify against original SH instructions. */

/* Bytes8284..82BC end exclusive; primary phase7, executed. */

void Timer_IncrementSixteenthBytes(void)

{
  undefined *puVar1;
  uint uVar2;
  
  puVar1 = PTR_PTR_0001120c;
  for (uVar2 = *(uint *)PTR_PTR_00011208; uVar2 < *(uint *)puVar1; uVar2 = uVar2 + 1) {
    Timer_IncrementByteUntilFF(uVar2);
  }
  return;
}

