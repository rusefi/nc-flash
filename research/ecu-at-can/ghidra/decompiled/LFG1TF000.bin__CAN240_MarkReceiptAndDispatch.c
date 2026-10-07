/* Ghidra analysis output; verify against original SH instructions. */

/* Marks8F85/8F8B mask7F; tail1AD2E calls18074,17FA0,180F0,17F38,18008. NativeISR logical5/mailbox7
   minimumDLC8. Syntheticpayload notphysicalhealth; tcu-receive-recovery.txt. */

void CAN240_MarkReceiptAndDispatch(void)

{
  undefined *puVar1;
  undefined *puVar2;
  
  (*(code *)PTR_FUN_0001c320)();
  puVar2 = PTR_FUN_0001c32c;
  puVar1 = PTR_DAT_0001c328;
  *PTR_DAT_0001c324 = *PTR_DAT_0001c324 | 0x7f;
  *puVar1 = *puVar1 | 0x7f;
  (*(code *)puVar2)();
                    /* WARNING: Could not recover jumptable at 0x0001c206. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*(code *)PTR_LAB_0001c330)();
  return;
}

