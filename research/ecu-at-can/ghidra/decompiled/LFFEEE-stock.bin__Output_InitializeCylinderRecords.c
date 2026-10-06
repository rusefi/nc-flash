/* Ghidra analysis output; verify against original SH instructions. */

/* Initialize four40-byte records53DC,channel IDs and deadlines from2F3B4/C4;clear mask
   cache5486,set5489. Executed in output-inhibition.txt. */

void Output_InitializeCylinderRecords(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined4 uVar4;
  undefined1 *puVar5;
  int iVar6;
  
  uVar4 = DAT_0001fc6c;
  puVar1 = PTR_DAT_0001fc5c;
  iVar6 = 0;
  *PTR_DAT_0001fc54 = 0;
  *(undefined2 *)PTR_Output_CachedInhibitMask_0001fc58 = 0;
  *puVar1 = 1;
  puVar3 = PTR_Output_CylinderRecords_0001fc68;
  puVar2 = PTR_Output_InitialEventDeadlines_0001fc64;
  puVar1 = PTR_Output_CylinderChannelMap_0001fc60;
  do {
    puVar5 = puVar3 + iVar6 * 0x28;
    *puVar5 = 0;
    puVar5[1] = 0;
    puVar5[2] = 0;
    puVar5[3] = 0;
    *(undefined2 *)(puVar5 + 4) = 0;
    puVar5[6] = 0;
    puVar5[7] = 0;
    *(undefined4 *)(puVar5 + 8) = *(undefined4 *)(puVar2 + iVar6 * 4);
    puVar5[0xc] = (char)iVar6;
    puVar5[0x10] = puVar1[iVar6];
    puVar5[0x11] = 0;
    *(undefined4 *)(puVar5 + 0x14) = 0;
    *(undefined4 *)(puVar5 + 0x18) = 0;
    *(undefined4 *)(puVar5 + 0x1c) = uVar4;
    *(undefined4 *)(puVar5 + 0x20) = uVar4;
    iVar6 = iVar6 + 1;
    puVar5[0x24] = 0;
  } while (iVar6 < 4);
  (*(code *)PTR_FUN_0001fc70)();
  *(undefined2 *)PTR_DAT_0001fc74 = 0;
  *(undefined4 *)PTR_DAT_0001fc78 = 0;
  *PTR_DAT_0001fc7c = 0;
  return;
}

