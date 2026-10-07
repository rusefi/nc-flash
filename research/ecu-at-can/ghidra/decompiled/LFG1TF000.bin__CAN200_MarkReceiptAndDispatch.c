/* Ghidra analysis output; verify against original SH instructions. */

/* Marks8F87/8F8D mask40; tail1ACD2->176B0 copiesbyte6bit0 to88D0/sets88D1=2. NativeISR
   logical9/mailbox11 minimumDLC7. See tcu-receive-recovery.txt. */

void CAN200_MarkReceiptAndDispatch(void)

{
  undefined *puVar1;
  undefined *puVar2;
  
  (*(code *)PTR_FUN_0001c320)();
  puVar2 = PTR_DAT_0001c344;
  puVar1 = PTR_FUN_0001c32c;
  *PTR_DAT_0001c340 = *PTR_DAT_0001c340 | 0x40;
  *puVar2 = *puVar2 | 0x40;
  (*(code *)puVar1)();
                    /* WARNING: Could not recover jumptable at 0x0001c2a4. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*(code *)PTR_LAB_0001c350)();
  return;
}

