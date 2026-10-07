/* Ghidra analysis output; verify against original SH instructions. */

/* WARNING: Removing unreachable block (ram,0x0001b52c) */
/* OriginalISRprefix throughregisterrestore at1B7D4 beforeRTE.6144wholeapplicationRAM cases
   overlogical0/1/4/5/6/8/9, allmodebytes andDLCboundaries. FiniteHCANsamples;
   nooverrun/concurrency/physicalinterruptproof. See tcu-receive-recovery.txt. */

undefined8 HCAN_ReceiveInterrupt(void)

{
  undefined1 uVar1;
  byte bVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined *puVar5;
  undefined *puVar6;
  undefined4 in_r0;
  uint uVar7;
  ushort uVar8;
  char cVar9;
  undefined4 in_r1;
  undefined *puVar10;
  undefined1 *puVar11;
  undefined1 *puVar12;
  undefined1 *puVar13;
  int iVar14;
  byte bStack_5c;
  char cStack_50;
  
  puVar5 = PTR_DAT_0001b514;
  puVar4 = PTR_FUN_0001b510;
  puVar3 = PTR_FUN_0001b50c;
  puVar13 = (undefined1 *)(int)DAT_0001b4fa;
  iVar14 = (int)DAT_0001b4fc;
  (*(code *)PTR_FUN_0001b510)(3);
  do {
    uVar8 = *(ushort *)(iVar14 + 0xe);
    if ((byte)uVar8 == 0) {
      if ((DAT_0001b500 & uVar8) == 0) {
        puVar10 = PTR_DAT_0001b518;
        uVar7 = (*(code *)PTR_FixedPoint_ShiftSignedBy12_0001b524)
                          (PTR_DAT_0001b518,PTR_DAT_0001b520);
        cStack_50 = puVar10[uVar7 & 0xff] + '\f';
      }
      else {
        puVar10 = PTR_DAT_0001b518;
        uVar7 = (*(code *)PTR_FUN_0001b51c)();
        cStack_50 = puVar10[uVar7 & 0xff] + '\b';
      }
    }
    else if ((uVar8 & 0xf) == 0) {
      cStack_50 = PTR_DAT_0001b518[(int)((uint)uVar8 & (int)DAT_0001b4fe) >> 4 & 0xff] + '\x04';
    }
    else {
      cStack_50 = PTR_DAT_0001b518[(byte)uVar8 & 0xf];
    }
    uVar8 = (*(code *)PTR_FUN_0001b528)();
    bStack_5c = cStack_50 + 8U & 0xf;
    (*(code *)puVar4)(4);
    do {
      puVar11 = (undefined1 *)((uint)bStack_5c * 8 + iVar14 + 0x20);
      *puVar13 = *puVar11;
      puVar13[2] = puVar11[4];
      puVar13[3] = puVar11[5];
      puVar11 = (undefined1 *)((uint)bStack_5c * 8 + DAT_0001b622 + iVar14);
      puVar13[4] = *puVar11;
      puVar13[5] = puVar11[1];
      puVar13[6] = puVar11[2];
      puVar13[7] = puVar11[3];
      puVar13[8] = puVar11[4];
      puVar13[9] = puVar11[5];
      puVar13[10] = puVar11[6];
      puVar13[0xb] = puVar11[7];
      if ((uVar8 & *(ushort *)(iVar14 + 0x1a)) == 0) break;
      *(ushort *)(iVar14 + 0x1a) = uVar8;
      cVar9 = (*(code *)PTR_FUN_0001b624)(4);
    } while (cVar9 != '\0');
    (*(code *)puVar3)(4);
    *(ushort *)(iVar14 + 0xe) = uVar8;
    *(ushort *)(iVar14 + 0x1a) = uVar8;
    *(undefined1 **)puVar5 = puVar13;
    puVar10 = PTR_HCAN_RxCopyLengthTable_0001b6f8;
    if (bStack_5c == 0) {
      bStack_5c = 1;
      do {
        bStack_5c = bStack_5c - 1;
        if (*(short *)(puVar13 + 2) == *(short *)(PTR_HCAN_RxIdTable_0001b628 + (uint)bStack_5c * 2)
           ) break;
      } while (bStack_5c != 0);
      if (*(short *)(puVar13 + 2) == *(short *)(PTR_HCAN_RxIdTable_0001b628 + (uint)bStack_5c * 2))
      goto CAN_RX_CopySliceStart;
    }
    else {
CAN_RX_CopySliceStart:
      bVar2 = PTR_HCAN_RxIndexTable_0001b6f4[bStack_5c];
      if (((byte)PTR_HCAN_RxCopyLengthTable_0001b6f8[bVar2] <= **(byte **)puVar5) &&
         (cVar9 = (*(code *)PTR_CAN_AdmitApplicationReceipt_0001b6fc)((int)(char)bVar2,puVar13 + 4),
         puVar6 = PTR_DAT_0001b700, cVar9 != '\0')) {
        if (*(int *)(PTR_DAT_0001b700 + (uint)bVar2 * 4) != 0) {
          *PTR_DAT_0001b704 = bVar2;
          cVar9 = (**(code **)(puVar6 + (uint)bVar2 * 4))(puVar13 + 4);
          if (cVar9 == '\0') goto LAB_0001b798;
        }
        if (*(int *)(PTR_HCAN_RxBufferTable_0001b708 + (uint)bVar2 * 4) != 0) {
          puVar12 = *(undefined1 **)(PTR_HCAN_RxBufferTable_0001b708 + (uint)bVar2 * 4);
          cVar9 = puVar10[bVar2];
          puVar11 = puVar13 + 4;
          if (cVar9 == '\b') {
            uVar1 = *puVar11;
            puVar11 = puVar13 + 5;
            *puVar12 = uVar1;
            puVar12 = puVar12 + 1;
LAB_0001b712:
            uVar1 = *puVar11;
            puVar11 = puVar11 + 1;
            *puVar12 = uVar1;
            puVar12 = puVar12 + 1;
LAB_0001b718:
            uVar1 = *puVar11;
            puVar11 = puVar11 + 1;
            *puVar12 = uVar1;
            puVar12 = puVar12 + 1;
LAB_0001b71e:
            uVar1 = *puVar11;
            puVar11 = puVar11 + 1;
            *puVar12 = uVar1;
            puVar12 = puVar12 + 1;
LAB_0001b724:
            uVar1 = *puVar11;
            puVar11 = puVar11 + 1;
            *puVar12 = uVar1;
            puVar12 = puVar12 + 1;
LAB_0001b72a:
            uVar1 = *puVar11;
            puVar11 = puVar11 + 1;
            *puVar12 = uVar1;
            puVar12 = puVar12 + 1;
LAB_0001b730:
            uVar1 = *puVar11;
            puVar11 = puVar11 + 1;
            *puVar12 = uVar1;
            puVar12 = puVar12 + 1;
          }
          else {
            if (cVar9 == '\a') goto LAB_0001b712;
            if (cVar9 == '\x06') goto LAB_0001b718;
            if (cVar9 == '\x05') goto LAB_0001b71e;
            if (cVar9 == '\x04') goto LAB_0001b724;
            if (cVar9 == '\x03') goto LAB_0001b72a;
            if (cVar9 == '\x02') goto LAB_0001b730;
            if (cVar9 != '\x01') goto LAB_0001b750;
          }
          *puVar12 = *puVar11;
        }
LAB_0001b750:
        PTR_DAT_0001b7e4[(byte)PTR_DAT_0001b7dc[bVar2]] =
             PTR_DAT_0001b7e4[(byte)PTR_DAT_0001b7dc[bVar2]] | PTR_DAT_0001b7e0[bVar2];
      }
    }
LAB_0001b798:
    if ((*(short *)(iVar14 + 0xe) == 0) || (cVar9 = (*(code *)PTR_FUN_0001b7e8)(3), cVar9 == '\0'))
    {
      (*(code *)puVar3)(3);
      return CONCAT44(in_r1,in_r0);
    }
  } while( true );
}

