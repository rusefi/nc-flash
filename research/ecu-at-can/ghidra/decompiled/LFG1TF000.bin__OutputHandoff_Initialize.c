/* Ghidra analysis output; verify against original SH instructions. */

/* Executes channel gains and correction-state initialization plus18942 checksum/bounded calibration
   loading. No fullboot or persistence claim. */

void OutputHandoff_Initialize(void)

{
  undefined2 uVar1;
  undefined *puVar2;
  int iVar3;
  int iVar4;
  undefined4 *puVar5;
  undefined1 *puVar6;
  ushort uVar7;
  int iVar8;
  int iVar9;
  int iVar10;
  
  puVar2 = PTR_DAT_0001888c;
  iVar4 = 0;
  puVar6 = (undefined1 *)(int)DAT_0001885c;
  puVar5 = (undefined4 *)(int)DAT_0001885e;
  uVar7 = 0;
  iVar8 = (int)DAT_00018860;
  iVar9 = (int)DAT_00018862;
  iVar10 = (int)DAT_00018864;
  do {
    uVar1 = *(undefined2 *)(puVar2 + iVar4);
    *(undefined2 *)(DAT_00018866 + iVar4) = uVar1;
    *(undefined2 *)(iVar4 + iVar10) = uVar1;
    uVar1 = *(undefined2 *)(PTR_DAT_00018890 + iVar4);
    *(undefined2 *)(iVar4 + iVar8) = uVar1;
    *(undefined2 *)(iVar4 + iVar9) = uVar1;
    iVar3 = (int)DAT_00018868;
    uVar1 = *(undefined2 *)(PTR_DAT_00018894 + iVar4);
    *(undefined2 *)(DAT_0001886a + iVar4) = uVar1;
    *(undefined2 *)(iVar3 + iVar4) = uVar1;
    *(undefined2 *)(iVar4 + DAT_0001886c) = 100;
    *(undefined2 *)(iVar4 + DAT_0001886e) = 0;
    *(undefined2 *)(iVar4 + DAT_00018870) = 0;
    *puVar5 = 0;
    *puVar6 = 0;
    uVar7 = uVar7 + 1;
    puVar6 = puVar6 + 1;
    *(undefined2 *)(iVar4 + DAT_00018872) = 0;
    puVar5 = puVar5 + 1;
    iVar4 = iVar4 + 2;
  } while (uVar7 < 4);
  *(undefined2 *)(int)DAT_00018874 = 100;
  *(undefined2 *)(int)DAT_00018876 = 0xff9c;
  *(undefined2 *)(int)DAT_00018878 = 0x32;
  *(undefined2 *)(int)DAT_0001887a = 0xffce;
  OutputHandoff_LoadCalibration();
  uVar1 = DAT_0001887c;
  *(undefined **)PTR_DAT_0001889c = PTR_DAT_00018898;
  *(undefined2 *)(int)DAT_0001887e = uVar1;
  *(undefined2 *)(int)DAT_00018880 = 1;
  *(undefined2 *)(int)DAT_00018882 = 3;
  *(undefined1 *)(int)DAT_00018884 = 0;
  *(undefined2 *)(int)DAT_00018886 = 0;
  return;
}

