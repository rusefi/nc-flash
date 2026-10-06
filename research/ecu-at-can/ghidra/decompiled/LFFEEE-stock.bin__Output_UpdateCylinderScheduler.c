/* Ghidra analysis output; verify against original SH instructions. */

/* Full caller reads736A via1F864;on change calls20290 then caches5486 even if deferred.16 mask
   cases,3 deferred lifecycle points and6 paired CAN211/TCU216-to-register paths. */

uint Output_UpdateCylinderScheduler(byte param_1)

{
  int iVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  short sVar7;
  undefined1 uVar9;
  byte bVar10;
  uint uVar5;
  int iVar6;
  undefined2 uVar8;
  undefined1 *puVar11;
  undefined *puVar12;
  char *pcVar13;
  byte *pbVar14;
  uint uVar15;
  char cVar16;
  int iVar17;
  char *pcVar18;
  int *piVar19;
  undefined *puVar20;
  char *pcVar21;
  int iVar22;
  
  uVar15 = (uint)param_1;
  *PTR_DAT_0001fc80 = param_1;
  puVar2 = PTR_DAT_0001fc74;
  iVar1 = DAT_0001fc6c;
  if (0x17 < uVar15) {
    uVar15 = uVar15 - 0x18;
  }
  iVar22 = uVar15 * DAT_0001fc84;
  if (*PTR_DAT_0001fc5c == '\x01') {
    *PTR_DAT_0001fc5c = 0;
    puVar12 = PTR_Output_CachedInhibitMask_0001fc58;
    *PTR_DAT_0001fc54 = 0;
    *(undefined2 *)puVar12 = 0;
    *(undefined2 *)puVar2 = 0;
    puVar3 = PTR_DAT_0001fc88;
    puVar12 = PTR_Output_CylinderRecords_0001fc68;
    *(undefined4 *)PTR_DAT_0001fc78 = 0;
    for (; puVar4 = PTR_DAT_0001fc88, puVar20 = PTR_Output_CylinderRecords_0001fc68,
        puVar12 < puVar3; puVar12 = puVar12 + 0x28) {
      *puVar12 = 0;
      puVar12[1] = 0;
      puVar12[6] = 0;
      puVar12[7] = 0;
      *(undefined2 *)(puVar12 + 4) = 0;
      puVar12[3] = 0;
      puVar12[2] = 0;
      for (puVar11 = puVar12 + 0x10; puVar11 < puVar12 + 0x28; puVar11 = puVar11 + 0x18) {
        *(undefined4 *)(puVar11 + 4) = 0;
        *(undefined4 *)(puVar11 + 8) = 0;
        *(int *)(puVar11 + 0xc) = iVar1;
        *(int *)(puVar11 + 0x10) = iVar1;
        puVar11[0x14] = 0;
        puVar11[1] = 0;
      }
    }
    for (; puVar20 < puVar4; puVar20 = puVar20 + 0x28) {
      iVar6 = Output_ForwardPositionDistance(iVar22,*(undefined4 *)(puVar20 + 8));
      (*(code *)PTR_FUN_0001fc8c)(puVar20);
      iVar17 = 0;
      for (puVar12 = puVar20 + 0x10; puVar12 < puVar20 + 0x28; puVar12 = puVar12 + 0x18) {
        if (iVar17 < *(int *)(puVar12 + 0x10)) {
          iVar17 = *(int *)(puVar12 + 0x10);
        }
      }
      if ((iVar6 < iVar17) || (DAT_0001fc6c <= iVar6)) {
        *(undefined2 *)(puVar20 + 4) = 0;
        puVar20[3] = 0;
        uVar9 = 2;
      }
      else {
        uVar8 = (*(code *)PTR_FUN_0001fc90)((int)*(short *)puVar2,1);
        puVar12 = PTR_FUN_0001fc98;
        *(undefined2 *)puVar2 = uVar8;
        sVar7 = (*(code *)puVar12)();
        *(short *)(puVar20 + 4) = sVar7 + 1;
        puVar20[3] = 1;
        uVar9 = 0;
      }
      puVar20[2] = uVar9;
    }
  }
  bVar10 = (*(code *)PTR_FUN_0001fda0)();
  if (bVar10 != *PTR_DAT_0001fda4) {
    FUN_0002013c(iVar22,(int)(char)PTR_DAT_0001fda8[bVar10]);
    *PTR_DAT_0001fda4 = bVar10;
  }
  uVar5 = (*(code *)PTR_Pattern_GetCylinderInhibitMask_0001fdac)();
  uVar15 = uVar5;
  if ((uVar5 & 0xffff) != (uint)*(ushort *)PTR_Output_CachedInhibitMask_0001fdb0) {
    uVar15 = Output_ApplyChangedInhibitMask(iVar22,uVar5);
    *(short *)PTR_Output_CachedInhibitMask_0001fdb0 = (short)uVar5;
  }
  pcVar13 = PTR_Output_CylinderRecords_0001fdb4 + DAT_0001fd9e;
  pcVar21 = PTR_Output_CylinderRecords_0001fdb4;
  do {
    if (pcVar13 <= pcVar21) {
      return uVar15;
    }
    iVar6 = Output_ForwardPositionDistance(iVar22,*(undefined4 *)(pcVar21 + 8));
    if (iVar1 <= iVar6) {
      for (pcVar18 = pcVar21 + 0x10; puVar3 = PTR_FUN_0001fdb8, puVar12 = PTR_DAT_0001fda4,
          pcVar18 < pcVar21 + 0x28; pcVar18 = pcVar18 + 0x18) {
        pcVar18[1] = '\0';
        (*(code *)puVar3)((int)*pcVar18);
      }
      pcVar21[2] = '\0';
      pcVar21[7] = '\0';
      puVar3 = PTR_Output_CylinderMaskBits_0001fdbc;
      *pcVar21 = PTR_DAT_0001fda8[(byte)*puVar12];
      pcVar21[1] = (*(ushort *)(puVar3 + (uint)(byte)pcVar21[0xc] * 2) &
                   *(ushort *)PTR_Output_CachedInhibitMask_0001fdb0) != 0;
      pcVar21[3] = '\0';
    }
    uVar15 = (uint)pcVar21[2];
    piVar19 = (int *)(PTR_Output_SchedulerModes_0001fdc0 + *pcVar21 * 0x10);
    if (uVar15 == 0) {
      cVar16 = '\x01';
      for (pbVar14 = (byte *)(pcVar21 + 0x10); pbVar14 < pcVar21 + 0x28; pbVar14 = pbVar14 + 0x18) {
        if (PTR_DAT_0001fdc4[(uint)*pbVar14 * 0x18] != '\0') {
          cVar16 = '\0';
          break;
        }
      }
      uVar15 = (uint)cVar16;
      if (uVar15 == 1) {
        if (piVar19[1] < iVar6) {
          if (iVar6 <= *piVar19) {
            if (pcVar21[3] == '\0') {
              uVar8 = (*(code *)PTR_FUN_0001fed8)((int)*(short *)puVar2,1);
              *(undefined2 *)puVar2 = uVar8;
              *(undefined2 *)(pcVar21 + 4) = *(undefined2 *)puVar2;
              pcVar21[3] = '\x01';
            }
            uVar15 = (uint)pcVar21[1];
            if (uVar15 == 0) {
              (*(code *)PTR_FUN_0001fedc)(pcVar21);
              for (pcVar18 = pcVar21 + 0x10; pcVar18 < pcVar21 + 0x28; pcVar18 = pcVar18 + 0x18) {
                *(undefined4 *)(pcVar18 + 0xc) = *(undefined4 *)(pcVar18 + 0x10);
              }
              (*(code *)PTR_FUN_0001fee0)(pcVar21);
              uVar15 = (*(code *)piVar19[2])(pcVar21,iVar6);
            }
          }
        }
        else {
          uVar15 = 2;
          pcVar21[2] = '\x02';
        }
      }
    }
    else if (((uVar15 == 1) && (uVar15 = (uint)pcVar21[1], uVar15 == 0)) &&
            (uVar15 = (uint)(byte)pcVar21[6], uVar15 == 1)) {
      (*(code *)PTR_FUN_0001fee0)(pcVar21);
      uVar15 = (*(code *)piVar19[2])(pcVar21,iVar6);
    }
    pcVar21 = pcVar21 + 0x28;
  } while( true );
}

