/* Ghidra analysis output; verify against original SH instructions. */

/* 20allRAMcases; initialtags0107,payloadROM5FCB4, bounds5FCA4/5FCAC, driverwords200,
   accumulators/flagszero. DoesnotinitializeA5DC. tcu-output-service.txt. */

void OutputRecord_InitFourChannels(void)

{
  undefined2 uVar1;
  undefined2 uVar2;
  int iVar3;
  undefined2 *puVar4;
  int iVar5;
  int iVar6;
  byte bVar7;
  undefined1 *puVar8;
  undefined4 *puVar9;
  undefined *puVar10;
  
  uVar1 = DAT_00052f6e;
  puVar8 = (undefined1 *)(int)DAT_00052f6a;
  bVar7 = 0;
  puVar9 = (undefined4 *)(int)DAT_00052f6c;
  puVar10 = PTR_DAT_00052f88;
  do {
    uVar2 = DAT_00052f70;
    iVar6 = (uint)bVar7 * 2;
    puVar4 = (undefined2 *)(PTR_OutputDriver_CurrentWords_00052f8c + iVar6);
    *(undefined2 *)(PTR_OutputDriver_PreviousWords_00052f90 + iVar6) = DAT_00052f70;
    *puVar4 = uVar2;
    *puVar10 = 0;
    *(undefined2 *)(iVar6 + DAT_00052f72) = 100;
    *(undefined2 *)(PTR_DAT_00052f94 + iVar6) = uVar1;
    *(undefined2 *)(PTR_DAT_00052f98 + iVar6) = *(undefined2 *)(PTR_DAT_00052f9c + iVar6);
    iVar3 = (int)DAT_00052f74;
    *(undefined2 *)(iVar3 + iVar6) = *(undefined2 *)(PTR_DAT_00052fa0 + iVar6);
    iVar5 = (int)DAT_00052f76;
    *(undefined2 *)(iVar5 + iVar6) = *(undefined2 *)(iVar6 + DAT_00052fa4);
    *(undefined2 *)(iVar6 + DAT_00052f78) = 0;
    *(undefined2 *)(iVar6 + DAT_00052f7a) = *(undefined2 *)(iVar3 + iVar6);
    *(undefined2 *)(iVar6 + DAT_00052f7c) = *(undefined2 *)(iVar5 + iVar6);
    *puVar9 = 0;
    *(undefined2 *)(iVar6 + DAT_00052f7e) = 0;
    *puVar8 = 0;
    bVar7 = bVar7 + 1;
    puVar8 = puVar8 + 1;
    puVar9 = puVar9 + 1;
    puVar10 = puVar10 + 1;
  } while (bVar7 < 4);
  *(undefined1 *)(int)DAT_00052f80 = 0;
  return;
}

