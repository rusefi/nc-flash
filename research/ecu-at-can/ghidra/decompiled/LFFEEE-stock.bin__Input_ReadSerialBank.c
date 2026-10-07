/* Ghidra analysis output; verify against original SH instructions. */

/* Executed local-inputs.txt and complete18DC8 tasks in control-task-serial.txt.144 new setup
   cases:PHDR bits14/15 bank selection, SCR/SMR/BRR/SDCR exactwrites, real786E(FF); syntheticpeer,
   no physical timing/wiring proof. */

int Input_ReadSerialBank(char param_1)

{
  bool bVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  char cVar5;
  int iVar6;
  int iVar7;
  int iVar8;
  byte *pbVar9;
  undefined4 local_34;
  undefined4 local_30;
  undefined4 local_2c;
  char cStack_28;
  undefined4 uStack_24;
  
  cStack_28 = param_1;
  uStack_24 = (*(code *)PTR_FUN_000077c0)((int)DAT_000077a0);
  puVar3 = PTR_FUN_000077b8;
  iVar7 = (int)DAT_0000779e;
  (*(code *)PTR_FUN_000077b8)(&local_2c,iVar7);
  pbVar9 = (byte *)(int)DAT_000077a2;
  *pbVar9 = *pbVar9 & 0xb;
  (*(code *)PTR_FUN_000077bc)(local_2c);
  (*(code *)puVar3)(&local_30,iVar7);
  cVar5 = (char)DAT_000077a4;
  *(char *)(int)DAT_000077a6 = cVar5;
  *pbVar9 = *pbVar9 & 0xfc;
  *(char *)(int)DAT_000077a8 = cVar5 + 'r';
  *(undefined1 *)(int)DAT_000077aa = 4;
  (*(code *)PTR_FUN_000077bc)(local_30);
  puVar4 = PTR_LAB_000077c4;
  puVar2 = PTR_Register_UpdateMaskedWord_000077b4;
  iVar6 = (int)DAT_000077ac;
  iVar8 = (int)DAT_000077ae;
  if (cStack_28 == '\0') {
    (*(code *)PTR_Register_UpdateMaskedWord_000077b4)(iVar8,iVar6,0);
    (*(code *)puVar2)(iVar8,puVar4,0);
  }
  else {
    bVar1 = cStack_28 != '\x01';
    if (bVar1) {
      (*(code *)PTR_Register_UpdateMaskedWord_000077b4)(iVar8,iVar6,0);
    }
    else {
      (*(code *)PTR_Register_UpdateMaskedWord_000077b4)(iVar8,iVar6,1);
    }
    (*(code *)puVar2)(iVar8,puVar4,bVar1);
  }
  (*(code *)puVar3)(&local_34,iVar7);
  *pbVar9 = *pbVar9 & 0xb | 0x30;
  (*(code *)PTR_FUN_000077bc)(local_34);
  cStack_28 = Input_TransferSerialByte((int)DAT_000077b0);
  (*(code *)PTR_FUN_000077c8)(uStack_24);
  return (int)cStack_28;
}

