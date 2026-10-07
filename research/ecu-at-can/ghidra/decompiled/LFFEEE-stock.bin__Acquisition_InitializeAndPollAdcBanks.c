/* Ghidra analysis output; verify against original SH instructions. */

/* 96originalcases PASS:finiteADFpollsamples at4B62/4B6C/4B76,32resultwords copied4008..4047
   plusflags/controls. WholeapplicationRAM/exactMMIO/order/preservedregisters checked.
   Explicitreadiness/results,no conversionlatency/IRQ. control-scheduler-start.txt. */

void Acquisition_InitializeAndPollAdcBanks(void)

{
  undefined2 uVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined2 *puVar4;
  undefined2 *puVar5;
  undefined2 *puVar6;
  byte *pbVar7;
  int iVar8;
  byte *pbVar9;
  byte *pbVar10;
  byte *pbVar11;
  undefined4 uStack_24;
  undefined4 uStack_20;
  undefined4 auStack_1c [2];
  
  puVar2 = PTR_FUN_00004c68;
  iVar8 = (int)DAT_00004c50;
  (*(code *)PTR_FUN_00004c68)(auStack_1c,iVar8);
  pbVar7 = (byte *)(int)DAT_00004c52;
  *pbVar7 = *pbVar7 & 0xdf;
  pbVar10 = (byte *)(int)DAT_00004c54;
  *pbVar10 = 0x33;
  *pbVar7 = *pbVar7 & 0x2f | 0x20;
  puVar3 = PTR_FUN_00004c6c;
  (*(code *)PTR_FUN_00004c6c)(auStack_1c[0]);
  (*(code *)puVar2)(&uStack_20,iVar8);
  pbVar7 = (byte *)(int)DAT_00004c56;
  *pbVar7 = *pbVar7 & 0xdf;
  pbVar11 = (byte *)(int)DAT_00004c58;
  *pbVar11 = 0x33;
  *pbVar7 = *pbVar7 & 0x2f | 0x20;
  (*(code *)puVar3)(uStack_20);
  (*(code *)puVar2)(&uStack_24,iVar8);
  pbVar7 = (byte *)(int)DAT_00004c5a;
  *pbVar7 = *pbVar7 & 0xdf;
  pbVar9 = (byte *)(int)DAT_00004c5c;
  *pbVar9 = 0x2b;
  *pbVar7 = *pbVar7 & 0x2f | 0x20;
  (*(code *)puVar3)(uStack_24);
  uVar1 = DAT_00004c5e;
  *PTR_Acquisition_AlternateArmed_00004c70 = 0;
  *PTR_Acquisition_PreviousScanMode_00004c74 = (char)uVar1;
  puVar2 = PTR_DAT_00004c78;
  PTR_DAT_00004c78[1] = 0;
  puVar2[4] = 0;
  puVar2[7] = 0;
  puVar2 = PTR_Acquisition_ADCResultBank_00004c7c;
  do {
  } while ((DAT_00004c60 & *pbVar10) == 0);
  do {
  } while ((DAT_00004c60 & *pbVar11) == 0);
  do {
  } while ((DAT_00004c60 & *pbVar9) == 0);
  puVar5 = (undefined2 *)(int)DAT_00004c62;
  *(undefined2 *)PTR_Acquisition_ADCResultBank_00004c7c = *puVar5;
  puVar4 = (undefined2 *)(int)DAT_00004c64;
  *(undefined2 *)(puVar2 + 2) = *puVar4;
  puVar6 = (undefined2 *)(int)DAT_00004c66;
  *(undefined2 *)(puVar2 + 4) = *puVar6;
  *(undefined2 *)(puVar2 + 6) = puVar5[3];
  *(undefined2 *)(puVar2 + 8) = puVar4[3];
  *(undefined2 *)(puVar2 + 10) = puVar6[3];
  *(undefined2 *)(puVar2 + 0xc) = puVar5[6];
  *(undefined2 *)(puVar2 + 0xe) = puVar4[6];
  *(undefined2 *)(puVar2 + 0x10) = puVar6[6];
  *(undefined2 *)(puVar2 + 0x12) = puVar5[9];
  *(undefined2 *)(puVar2 + 0x14) = puVar4[9];
  *(undefined2 *)(puVar2 + 0x16) = puVar6[9];
  *(undefined2 *)(puVar2 + 0x18) = puVar5[0x10];
  *(undefined2 *)(puVar2 + 0x1a) = puVar4[0x10];
  *(undefined2 *)(puVar2 + 0x1c) = puVar6[0x10];
  *(undefined2 *)(puVar2 + 0x1e) = puVar5[0x13];
  *(undefined2 *)(puVar2 + 0x20) = puVar4[0x13];
  *(undefined2 *)(puVar2 + 0x22) = puVar5[0x15];
  *(undefined2 *)(puVar2 + 0x24) = puVar4[0x15];
  *(undefined2 *)(puVar2 + 0x26) = puVar5[0x17];
  *(undefined2 *)(puVar2 + 0x28) = puVar4[0x17];
  *(undefined2 *)(puVar2 + 0x2a) = puVar5[0x19];
  *(undefined2 *)(puVar2 + 0x2c) = puVar4[0x19];
  *(undefined2 *)(puVar2 + 0x2e) = puVar5[0x1b];
  *(undefined2 *)(puVar2 + 0x30) = puVar4[0x1f];
  *(undefined2 *)(puVar2 + 0x32) = puVar5[0x21];
  *(undefined2 *)(puVar2 + 0x34) = puVar4[0x21];
  *(undefined2 *)(puVar2 + 0x36) = puVar5[0x23];
  *(undefined2 *)(puVar2 + 0x38) = puVar4[0x23];
  *(undefined2 *)(puVar2 + 0x3a) = puVar5[0x25];
  *(undefined2 *)(puVar2 + 0x3c) = puVar4[0x25];
  *(undefined2 *)(puVar2 + 0x3e) = puVar5[0x27];
  return;
}

