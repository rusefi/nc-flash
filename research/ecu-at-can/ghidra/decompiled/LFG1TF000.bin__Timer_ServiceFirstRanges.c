/* Ghidra analysis output; verify against original SH instructions. */

/* ROM76D24..76D40 defines four ranges; word countdown8420..844E includes843E/8440. 30000 actual
   calls executed in verify_selector_recovery.py; wall time and tick ratio not established. */

void Timer_ServiceFirstRanges(void)

{
  undefined *puVar1;
  undefined *puVar2;
  uint uVar3;
  
  puVar1 = PTR_PTR_00011b60;
  for (uVar3 = *(uint *)PTR_PTR_00011b5c; puVar2 = PTR_PTR_00011b68, uVar3 < *(uint *)puVar1;
      uVar3 = uVar3 + 1) {
    FUN_00011d74(uVar3);
  }
  for (uVar3 = *(uint *)PTR_PTR_00011b64; puVar1 = PTR_PTR_00011b70, uVar3 < *(uint *)puVar2;
      uVar3 = uVar3 + 2) {
    FUN_00011d88(uVar3);
  }
  for (uVar3 = *(uint *)PTR_PTR_00011b6c; puVar2 = PTR_PTR_00011b78, uVar3 < *(uint *)puVar1;
      uVar3 = uVar3 + 1) {
    FUN_00011d9c(uVar3);
  }
  for (uVar3 = *(uint *)PTR_PTR_00011b74; uVar3 < *(uint *)puVar2; uVar3 = uVar3 + 2) {
    Timer_DecrementWordUnlessSentinel(uVar3);
  }
  return;
}

