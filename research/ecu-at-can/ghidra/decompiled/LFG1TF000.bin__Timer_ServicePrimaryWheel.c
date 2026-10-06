/* Ghidra analysis output; verify against original SH instructions. */

/* Original16-slot wheel5C0F0; even old phase also increments90C8.1024 calls verified; no physical
   period claim. */

void Timer_ServicePrimaryWheel(void)

{
  uint uVar1;
  uint *puVar2;
  
  puVar2 = (uint *)(int)DAT_000110ea;
  if ((*puVar2 & 1) == 0) {
    (*(code *)PTR_Timer_IncrementPhaseCounter_000110f0)();
  }
  (**(code **)(PTR_Timer_PrimaryWheelTable_000110f4 + *puVar2 * 4))();
  uVar1 = *puVar2;
  *puVar2 = uVar1 + 1;
  if (uVar1 + 1 == 0x10) {
    *puVar2 = 0;
  }
  return;
}

