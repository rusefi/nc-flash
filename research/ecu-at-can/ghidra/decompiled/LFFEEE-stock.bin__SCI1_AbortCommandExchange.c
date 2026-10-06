/* Ghidra analysis output; verify against original SH instructions. */

/* Timeoutpath disablestransfer,setsPDDRbit0,completion2/active0. Rawpartialbuffers
   remain;freshstart resetsstate. */

void SCI1_AbortCommandExchange(void)

{
  undefined *puVar1;
  undefined *puVar2;
  int iVar3;
  undefined4 local_1c;
  undefined4 uStack_18;
  undefined4 auStack_14 [2];
  
  puVar1 = PTR_FUN_0000c5b8;
  iVar3 = (int)DAT_0000c5a8;
  (*(code *)PTR_FUN_0000c5b8)(auStack_14,iVar3);
  *(byte *)(int)DAT_0000c5b2 = *(byte *)(int)DAT_0000c5b2 & 0xb;
  puVar2 = PTR_FUN_0000c5bc;
  (*(code *)PTR_FUN_0000c5bc)(auStack_14[0]);
  (*(code *)puVar1)(&uStack_18,iVar3);
  *(byte *)(int)DAT_0000c5ac = *(byte *)(int)DAT_0000c5ac & 0x87 | 0x80;
  (*(code *)puVar2)(uStack_18);
  *(undefined2 *)(int)DAT_0000c5b4 = DAT_0000c5b6;
  (*(code *)puVar1)(&local_1c,iVar3);
  (*(code *)PTR_Register_UpdateMaskedWord_0000c5c8)((int)DAT_0000c5ae,1);
  (*(code *)puVar2)(local_1c);
  puVar1 = PTR_SCI1_ExchangeActive_0000c5cc;
  *PTR_SCI1_ExchangeCompletion_0000c5d4 = 2;
  *puVar1 = 0;
  return;
}

