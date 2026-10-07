/* Ghidra analysis output; verify against original SH instructions. */

/* 240wholeRAM cases PASS: SCI4F020..26 twoTX/twoexplicitRX bytes,
   signextended16bitreturn;25orderedSCI+8PFDR/PLIRaccesses, savedregisters/SR,
   unchangedapplicationRAM. ConstantSSR C0 fixture; SMR80/BRR2/SDCRFA, PLIRF75Cbit9 andPFDRbit11
   toggled. No externalpeer/timing/pinsproof. control-timer-event2.txt. */

int Control_ExchangeSerial4Word(undefined1 param_1,undefined1 param_2)

{
  byte bVar1;
  ushort uVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined *puVar5;
  char cVar6;
  byte *pbVar7;
  int iVar8;
  byte *pbVar9;
  undefined4 local_50;
  undefined4 uStack_4c;
  undefined4 local_48;
  undefined4 local_44;
  undefined4 local_40;
  undefined4 local_3c;
  undefined4 local_38;
  undefined4 local_34;
  undefined4 uStack_30;
  undefined4 local_2c;
  undefined4 uStack_28;
  byte bStack_24;
  
  puVar3 = PTR_FUN_0000bd90;
  iVar8 = (int)DAT_0000bd74;
  bStack_24 = param_2;
  (*(code *)PTR_FUN_0000bd90)(&uStack_28,iVar8);
  (*(code *)puVar3)(&local_2c,iVar8);
  cVar6 = (char)DAT_0000bd76;
  *(char *)(int)DAT_0000bd78 = cVar6;
  pbVar7 = (byte *)(int)DAT_0000bd7a;
  *pbVar7 = *pbVar7 & 0xfc;
  *(char *)(int)DAT_0000bd7c = cVar6 + 'z';
  *(undefined1 *)(int)DAT_0000bd7e = 2;
  puVar4 = PTR_FUN_0000bd94;
  (*(code *)PTR_FUN_0000bd94)(local_2c);
  puVar5 = PTR_Register_UpdateMaskedWord_0000bd98;
  (*(code *)PTR_Register_UpdateMaskedWord_0000bd98)((int)DAT_0000bd82,(int)DAT_0000bd80,1);
  (*(code *)puVar3)(&uStack_30,iVar8);
  (*(code *)puVar5)((int)DAT_0000bd86,(int)DAT_0000bd84,0);
  (*(code *)puVar4)(uStack_30);
  (*(code *)puVar3)(&local_34,iVar8);
  *pbVar7 = *pbVar7 & 0xb | 0x30;
  (*(code *)puVar4)(local_34);
  (*(code *)puVar3)(&local_38,iVar8);
  pbVar9 = (byte *)(int)DAT_0000bd88;
  *pbVar9 = *pbVar9 & 0x87 | 0x80;
  (*(code *)puVar4)(local_38);
  (*(code *)puVar3)(&local_3c,iVar8);
  *(undefined1 *)(int)DAT_0000bd8a = param_1;
  *pbVar9 = *pbVar9 & 0x7f | 0x78;
  (*(code *)puVar4)(local_3c);
  do {
  } while ((*pbVar9 & 0x40) == 0);
  (*(code *)puVar3)(&local_40,iVar8);
  bVar1 = *(byte *)(int)DAT_0000bd8c;
  *pbVar9 = *pbVar9 & 0xbf | 0xb8;
  (*(code *)puVar4)(local_40);
  (*(code *)puVar3)(&local_44,iVar8);
  *(byte *)(int)DAT_0000bd8a = bStack_24;
  *pbVar9 = *pbVar9 & 0x7f | 0x78;
  (*(code *)puVar4)(local_44);
  do {
  } while ((*pbVar9 & 0x40) == 0);
  (*(code *)puVar3)(&local_48,iVar8);
  bStack_24 = *(byte *)(int)DAT_0000bd8c;
  *pbVar9 = *pbVar9 & 0xbf | 0xb8;
  (*(code *)puVar4)(local_48);
  uVar2 = (ushort)bStack_24;
  (*(code *)puVar3)(&uStack_4c,iVar8);
  (*(code *)puVar5)((int)DAT_0000bd86,(int)DAT_0000bd84,1);
  (*(code *)puVar4)(uStack_4c);
  (*(code *)puVar5)((int)DAT_0000bd82,(int)DAT_0000bd80,0);
  (*(code *)puVar3)(&local_50,iVar8);
  *pbVar7 = *pbVar7 & 0xb;
  (*(code *)puVar4)(local_50);
  (*(code *)puVar4)(uStack_28);
  return (int)(short)((ushort)bVar1 * 0x100 + uVar2);
}

