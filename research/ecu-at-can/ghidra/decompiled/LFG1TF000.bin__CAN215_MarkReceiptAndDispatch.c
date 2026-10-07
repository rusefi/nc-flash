/* Ghidra analysis output; verify against original SH instructions. */

/* Logical6 callback OR80/FF/03 into8F85..87 and8F8B..8D, then1ACF0.
   OriginalISRprefixmailbox8->native1BD10->thiscallback executesin352fulltasks
   andtwoCAN215expiry/recoverychains; tcu-receive-admission.txt. */

void CAN215_MarkReceiptAndDispatch(void)

{
  undefined2 uVar1;
  undefined *puVar2;
  undefined *puVar3;
  
  (*(code *)PTR_FUN_0001c320)();
  puVar3 = PTR_DAT_0001c334;
  puVar2 = PTR_FUN_0001c32c;
  uVar1 = DAT_0001c314;
  PTR_DAT_0001c334[3] = PTR_DAT_0001c334[3] | 0x80;
  puVar3[4] = (char)uVar1;
  puVar3[5] = puVar3[5] | 3;
  puVar3 = PTR_DAT_0001c338;
  PTR_DAT_0001c338[3] = PTR_DAT_0001c338[3] | 0x80;
  puVar3[4] = (char)uVar1;
  puVar3[5] = puVar3[5] | 3;
  (*(code *)puVar2)();
                    /* WARNING: Could not recover jumptable at 0x0001c23e. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*(code *)PTR_CAN215_ConvertFields_0001c33c)();
  return;
}

