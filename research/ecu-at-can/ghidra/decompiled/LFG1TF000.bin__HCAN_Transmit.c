/* Ghidra analysis output; verify against original SH instructions. */

/* WARNING: Removing unreachable block (ram,0x0001b360) */
/* IDs5C864, DLC5C86E, buffers5C874. HCAN baseFFFFE400; register ID byte order differs from CPU. */

undefined4 HCAN_Transmit(byte param_1,byte param_2)

{
  undefined *puVar1;
  char cVar4;
  undefined2 uVar3;
  undefined4 uVar2;
  undefined1 *puVar5;
  undefined1 *puVar6;
  int iVar7;
  int iVar8;
  
  iVar7 = (int)DAT_0001b3bc;
  *(undefined2 *)(iVar7 + DAT_0001b3be) =
       *(undefined2 *)(PTR_HCAN_TxIdTable_0001b3c8 + (uint)param_2 * 2);
  *(undefined *)(DAT_0001b3c0 + iVar7) = PTR_HCAN_TxDlcTable_0001b3cc[param_2];
  iVar8 = (uint)param_2 * 4;
  if ((*(int *)(PTR_DAT_0001b3d0 + iVar8) == 0) ||
     (cVar4 = (**(code **)(PTR_DAT_0001b3d0 + iVar8))(DAT_0001b3c2 + iVar7 + (uint)param_1 * 8),
     cVar4 != '\0')) {
    puVar5 = *(undefined1 **)(PTR_HCAN_TxBufferTable_0001b3d4 + iVar8);
    puVar6 = (undefined1 *)(DAT_0001b3c2 + iVar7 + (uint)param_1 * 8);
    *puVar6 = *puVar5;
    puVar6[1] = puVar5[1];
    puVar6[2] = puVar5[2];
    puVar6[3] = puVar5[3];
    puVar6[4] = puVar5[4];
    puVar6[5] = puVar5[5];
    puVar6[6] = puVar5[6];
    puVar6[7] = puVar5[7];
  }
  if ((PTR_DAT_0001b3d8[0xf - (uint)param_1] == param_2) && ((*PTR_DAT_0001b3dc & 1) != 0)) {
    uVar3 = (*(code *)PTR_FUN_0001b3e0)();
    puVar1 = PTR_FUN_0001b3e4;
    *(undefined2 *)(iVar7 + 6) = uVar3;
    (*(code *)puVar1)();
    uVar2 = 1;
  }
  else {
    PTR_DAT_0001b3d8[0xf - (uint)param_1] = (char)DAT_0001b3c6;
    uVar2 = 0;
  }
  return uVar2;
}

