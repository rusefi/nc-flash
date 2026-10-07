/* Ghidra analysis output; verify against original SH instructions. */

/* Sets30 in8F87/8F8D then1ACD8;1225 earlierdispatchcases. NoworiginalISRmailbox10/logical8
   ->native1BD10 ->thiscallback in352fulltasks; logical6 CAN215 and1 CAN4EC dispatchbefore201. See
   tcu-receive-admission.txt. */

void CAN201_MarkReceiptAndDispatch(void)

{
  undefined *puVar1;
  undefined *puVar2;
  
  (*(code *)PTR_FUN_0001c320)();
  puVar2 = PTR_DAT_0001c344;
  puVar1 = PTR_FUN_0001c32c;
  *PTR_DAT_0001c340 = *PTR_DAT_0001c340 | 0x30;
  *puVar2 = *puVar2 | 0x30;
  (*(code *)puVar1)();
                    /* WARNING: Could not recover jumptable at 0x0001c282. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*(code *)PTR_CAN201_ApplicationCallback_0001c34c)();
  return;
}

