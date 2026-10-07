/* Ghidra analysis output; verify against original SH instructions. */

/* WARNING: Removing unreachable block (ram,0x0001af9a) */
/* 256setup-index0 cases:
   independentwholeRAM/344HCAN+2PBCRHaccesses/fullconfiguration/registerchecks PASS. GSR8/0
   externalresetstates. BCR803E,MBCRFF0F,MBIMR0070,IMRBCEE,MCR80; originalmailboxclear/setup.
   Commandwritesrecordedwithoutinventedsideeffects; tcu-hcan-startup.txt. */

void HCAN_ConfigureControllerAndMailboxes(byte param_1)

{
  undefined2 uVar1;
  ushort uVar2;
  byte *pbVar3;
  char cVar5;
  int iVar4;
  undefined *puVar6;
  undefined *puVar7;
  byte *pbVar8;
  byte local_20;
  
  FUN_0001ae40();
  puVar6 = PTR_CANPort_EnablePbcrhBits_0001af5c;
  pbVar8 = (byte *)(int)DAT_0001af48;
  *(undefined2 *)(pbVar8 + 0x12) = DAT_0001af4c;
  (*(code *)puVar6)();
  *(undefined2 *)(pbVar8 + 2) = *(undefined2 *)(PTR_DAT_0001af60 + (uint)param_1 * 2);
  pbVar3 = pbVar8 + 0x20;
  cVar5 = (char)DAT_0001af4a;
  for (local_20 = cVar5; local_20 != '\0'; local_20 = local_20 + -1) {
    *pbVar3 = 0;
    pbVar3 = pbVar3 + 1;
  }
  pbVar3 = pbVar8 + DAT_0001af4e;
  for (local_20 = cVar5; local_20 != '\0'; local_20 = local_20 + -1) {
    *pbVar3 = 0;
    pbVar3 = pbVar3 + 1;
  }
  *(undefined2 *)(pbVar8 + 4) = DAT_0001af4c;
  uVar2 = (ushort)PTR_DAT_0001af64;
  *(ushort *)(pbVar8 + 8) = uVar2;
  pbVar8[0x12] = 0;
  pbVar8[0x13] = 1;
  *(ushort *)(pbVar8 + 10) = uVar2;
  *(short *)(pbVar8 + 0x16) = (short)PTR_DAT_0001af68;
  *(short *)(pbVar8 + 0x14) = (short)PTR_DAT_0001af6c;
  *(ushort *)(pbVar8 + 0x14) = *(ushort *)(pbVar8 + 0x14) & uVar2;
  *(undefined2 *)(pbVar8 + 0x24) = *(undefined2 *)PTR_DAT_0001af70;
  *(undefined2 *)(pbVar8 + 0x1e) = *(undefined2 *)(PTR_DAT_0001af74 + (uint)param_1 * 2);
  iVar4 = 0xb;
  puVar6 = PTR_HCAN_RxCopyLengthTable_0001af7c;
  puVar7 = PTR_HCAN_RxIdTable_0001af78;
  for (local_20 = 0; (int)(uint)local_20 < iVar4; local_20 = local_20 + 1) {
    uVar2 = (*(code *)PTR_FUN_0001b0a4)();
    *(ushort *)(pbVar8 + 0x14) = *(ushort *)(pbVar8 + 0x14) & ~uVar2;
    *(undefined2 *)(pbVar8 + (uint)(byte)(local_20 + 1) * 8 + 0x24) =
         *(undefined2 *)(puVar7 + (uint)(byte)(local_20 + 1) * 2);
    pbVar8[(uint)(byte)(local_20 + 1) * 8 + 0x20] = puVar6[(byte)(local_20 + 1)];
    uVar2 = (*(code *)PTR_FUN_0001b0a4)();
    *(ushort *)(pbVar8 + 4) = *(ushort *)(pbVar8 + 4) | uVar2;
  }
  *pbVar8 = *pbVar8 & 0xa3;
  *(ushort *)(pbVar8 + 0x14) = *(ushort *)(pbVar8 + 0x14) & (ushort)PTR_DAT_0001b0a8;
  puVar6 = PTR_DAT_0001b0ac;
  uVar1 = DAT_0001b09a;
  for (local_20 = 0xf; 0xe < local_20; local_20 = local_20 - 1) {
    puVar6[0xf - (uint)local_20] = (char)uVar1;
  }
  FUN_0001ae76();
  *(undefined2 *)(int)DAT_0001b09c = *(undefined2 *)(pbVar8 + 0x14);
  return;
}

