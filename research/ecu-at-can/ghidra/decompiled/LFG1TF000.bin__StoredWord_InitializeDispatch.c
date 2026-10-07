/* Ghidra analysis output; verify against original SH instructions. */

/* Original table5C284+40 dispatch to137B4 executed;5source-pattern cases and stock startup coupled
   traces. tcu-stored-adjustments.txt. */

void StoredWord_InitializeDispatch(void)

{
                    /* WARNING: Could not recover jumptable at 0x000137b0. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (**(code **)(PTR_DAT_000137d4 + 0x28))();
  return;
}

