/* Ghidra analysis output; verify against original SH instructions. */

/* Marks8F82/8F88 mask03; tail1AE0E->182A2 convertsbytes6/7. NativeISR logical0/mailbox2
   minimumDLC8. Syntheticpayload only; see tcu-receive-recovery.txt. */

void CAN4F1_MarkReceiptAndDispatch(void)

{
  undefined *puVar1;
  undefined *puVar2;
  
  (*(code *)PTR_FUN_0001c1b4)();
  puVar2 = PTR_DAT_0001c1c8;
  puVar1 = PTR_FUN_0001c1c0;
  *PTR_DAT_0001c1c4 = *PTR_DAT_0001c1c4 | 3;
  *puVar2 = *puVar2 | 3;
  (*(code *)puVar1)();
                    /* WARNING: Could not recover jumptable at 0x0001c10a. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*DAT_0001c1cc)();
  return;
}

