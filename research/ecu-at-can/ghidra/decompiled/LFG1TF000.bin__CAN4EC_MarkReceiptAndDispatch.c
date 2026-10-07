/* Ghidra analysis output; verify against original SH instructions. */

/* Logical1 dispatcher callback: ORFC/FF/03 into8F82..84 and8F88..8A, then1ADD0.
   Executednativefulltask beforelogical6/8; comparisoninitiallyold201. NotOEMsenderattribution;
   tcu-receive-admission.txt. */

void CAN4EC_MarkReceiptAndDispatch(void)

{
  undefined2 uVar1;
  undefined *puVar2;
  undefined *puVar3;
  
  (*(code *)PTR_FUN_0001c1b4)();
  puVar3 = PTR_DAT_0001c1c4;
  puVar2 = PTR_FUN_0001c1c0;
  uVar1 = DAT_0001c1ac;
  *PTR_DAT_0001c1c4 = *PTR_DAT_0001c1c4 | 0xfc;
  puVar3[1] = (char)uVar1;
  puVar3[2] = puVar3[2] | 3;
  puVar3 = PTR_DAT_0001c1c8;
  *PTR_DAT_0001c1c8 = *PTR_DAT_0001c1c8 | 0xfc;
  puVar3[1] = (char)uVar1;
  puVar3[2] = puVar3[2] | 3;
  (*(code *)puVar2)();
                    /* WARNING: Could not recover jumptable at 0x0001c142. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*(code *)PTR_Acquisition_RefreshSecondaryCANGroup_0001c1d0)();
  return;
}

