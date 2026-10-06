/* Ghidra analysis output; verify against original SH instructions. */

/* Sets0C in FFFF8F87/8F8D, then calls empty1ACEC. Executed from real dispatcher; no payload reads
   on tested paths. */

void CAN211_MarkReceipt(void)

{
  undefined *puVar1;
  undefined *puVar2;
  
  (*(code *)PTR_FUN_0001c320)();
  puVar2 = PTR_DAT_0001c344;
  puVar1 = PTR_FUN_0001c32c;
  *PTR_DAT_0001c340 = *PTR_DAT_0001c340 | 0xc;
  *puVar2 = *puVar2 | 0xc;
  (*(code *)puVar1)();
                    /* WARNING: Could not recover jumptable at 0x0001c260. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*(code *)PTR_CAN211_EmptyApplicationCallback_0001c348)();
  return;
}

