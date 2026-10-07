/* Ghidra analysis output; verify against original SH instructions. */

/* Checksum over lowRAM63B8..63C8 versus63CA; match clamps gains900..1100 and offsets-100..100,
   mismatch defaults1000/0. Executed, not EEPROM provenance. */

void OutputHandoff_LoadCalibration(void)

{
  undefined *puVar1;
  undefined2 uVar2;
  int iVar3;
  int iVar4;
  short sVar5;
  short sVar6;
  int iVar7;
  
  puVar1 = PTR_FUN_00018a38;
  uVar2 = DAT_000189ba;
  sVar5 = *DAT_000189d8 + DAT_000189b4;
  sVar6 = 0;
  iVar3 = 0;
  do {
    sVar6 = sVar6 + 1;
    sVar5 = *(short *)(iVar3 + DAT_000189dc) + sVar5 + *(short *)(iVar3 + DAT_000189dc + 8);
    iVar3 = iVar3 + 2;
  } while (sVar6 < 4);
  iVar3 = (int)DAT_000189b6;
  iVar7 = (int)DAT_000189b8;
  if (sVar5 == *DAT_000189e0) {
    iVar4 = 0;
    sVar5 = 0;
    do {
      uVar2 = (*(code *)puVar1)((int)*(short *)(iVar4 + DAT_00018a3c),(int)DAT_00018a34,
                                (int)DAT_00018a32);
      *(undefined2 *)(iVar4 + iVar3) = uVar2;
      uVar2 = (*(code *)puVar1)((int)*(short *)(iVar4 + DAT_00018a40),0xffffff9c,100);
      *(undefined2 *)(iVar4 + iVar7) = uVar2;
      sVar5 = sVar5 + 1;
      iVar4 = iVar4 + 2;
    } while (sVar5 < 4);
    *(undefined1 *)(int)DAT_00018a36 = 0;
  }
  else {
    iVar4 = 0;
    sVar5 = 0;
    do {
      *(undefined2 *)(iVar3 + iVar4) = uVar2;
      *(undefined2 *)(iVar7 + iVar4) = 0;
      sVar5 = sVar5 + 1;
      iVar4 = iVar4 + 2;
    } while (sVar5 < 4);
    *(undefined1 *)(int)DAT_000189bc = 1;
  }
  return;
}

