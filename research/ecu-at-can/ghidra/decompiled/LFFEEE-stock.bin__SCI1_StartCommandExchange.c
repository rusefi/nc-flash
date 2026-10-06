/* Ghidra analysis output; verify against original SH instructions. */

/* C00A target;reset sums/index/status,setactive43A9,enableSCR,clearPDDRbit0. FirstTDRwrite comes
   from subsequentbytecallback. */

void SCI1_StartCommandExchange(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  byte *pbVar4;
  int iVar5;
  undefined4 local_28;
  undefined4 local_24;
  undefined4 uStack_20;
  undefined4 local_1c;
  undefined4 uStack_18;
  
  uStack_18 = (*(code *)PTR_FUN_0000c46c)((int)DAT_0000c45a);
  puVar1 = PTR_FUN_0000c470;
  iVar5 = (int)DAT_0000c45c;
  (*(code *)PTR_FUN_0000c470)(&local_1c,iVar5);
  pbVar4 = (byte *)(int)DAT_0000c45e;
  *pbVar4 = *pbVar4 & 0xb;
  puVar2 = PTR_FUN_0000c474;
  (*(code *)PTR_FUN_0000c474)(local_1c);
  (*(code *)puVar1)(&uStack_20,iVar5);
  *(byte *)(int)DAT_0000c460 = *(byte *)(int)DAT_0000c460 & 0x87 | 0x80;
  (*(code *)puVar2)(uStack_20);
  *(undefined2 *)(int)DAT_0000c462 = DAT_0000c464;
  puVar3 = PTR_SCI1_TransmitByteSum_0000c47c;
  *PTR_SCI1_ExchangeActive_0000c478 = 1;
  *(undefined2 *)puVar3 = 0;
  puVar3 = PTR_SCI1_ExchangeByteIndex_0000c484;
  *(undefined2 *)PTR_SCI1_ReceiveByteSum_0000c480 = 0;
  *puVar3 = 0;
  puVar3 = PTR_SCI1_ExchangeCompletion_0000c48c;
  *PTR_DAT_0000c488 = 0;
  *puVar3 = 0;
  (*(code *)puVar1)(&local_24,iVar5);
  *pbVar4 = *pbVar4 & 0xb | 0x30;
  (*(code *)puVar2)(local_24);
  (*(code *)puVar1)(&local_28,iVar5);
  (*(code *)PTR_Register_UpdateMaskedWord_0000c490)((int)DAT_0000c466,1,0);
  (*(code *)puVar2)(local_28);
  (*(code *)PTR_FUN_0000c494)(uStack_18);
  return;
}

