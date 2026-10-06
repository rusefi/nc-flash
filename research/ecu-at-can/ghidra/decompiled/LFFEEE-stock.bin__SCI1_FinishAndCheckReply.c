/* Ghidra analysis output; verify against original SH instructions. */

/* PDDRbit0set;active43A9clear;sumfirst38+BEtrailer==5AA5mod65536 ->completion1 else2. */

undefined4 SCI1_FinishAndCheckReply(void)

{
  undefined *puVar1;
  undefined4 uVar2;
  undefined4 local_8 [2];
  
  (*(code *)PTR_FUN_0000c5b8)(local_8,(int)DAT_0000c5a8);
  (*(code *)PTR_Register_UpdateMaskedWord_0000c5c8)((int)DAT_0000c5ae,1);
  uVar2 = (*(code *)PTR_FUN_0000c5bc)(local_8[0]);
  puVar1 = PTR_DAT_0000c5d0;
  *PTR_SCI1_ExchangeActive_0000c5cc = 0;
  if (((int)*(short *)PTR_SCI1_ReceiveByteSum_0000c5c4 + (int)*(short *)puVar1 & 0xffffU) ==
      (int)DAT_0000c5b0) {
    uVar2 = 1;
    *PTR_SCI1_ExchangeCompletion_0000c5d4 = 1;
  }
  else {
    *PTR_SCI1_ExchangeCompletion_0000c5d4 = 2;
  }
  return uVar2;
}

