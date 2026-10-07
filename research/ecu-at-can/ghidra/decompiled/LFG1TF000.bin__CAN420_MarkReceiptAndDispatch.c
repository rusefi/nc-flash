/* Ghidra analysis output; verify against original SH instructions. */

/* Marks8F84/8F8A mask80; tail1AD4E->17158. NativeISR logical4/mailbox6 minimumDLC1. See
   tcu-receive-recovery.txt. */

void CAN420_MarkReceiptAndDispatch(void)

{
  undefined *puVar1;
  undefined *puVar2;
  
  (*(code *)PTR_FUN_0001c1b4)();
  puVar2 = PTR_DAT_0001c1d8;
  puVar1 = PTR_FUN_0001c1c0;
  *PTR_DAT_0001c1d4 = *PTR_DAT_0001c1d4 | 0x80;
  *puVar2 = *puVar2 | 0x80;
  (*(code *)puVar1)();
                    /* WARNING: Could not recover jumptable at 0x0001c1a8. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*(code *)PTR_LAB_0001c1e4)();
  return;
}

