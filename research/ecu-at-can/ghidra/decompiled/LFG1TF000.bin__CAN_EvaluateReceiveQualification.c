/* Ghidra analysis output; verify against original SH instructions. */

/* WARNING: Removing unreachable block (ram,0x0001a644) */
/* Actions0 initialize,14 recover,15 set expiry bit,1 evaluate (hex). Two per-record timer banks
   require mode+20==1; stock211/4B0/430 skipped. Seven enabled lifecycles verified;8EE2 not input to
   action1. */

uint CAN_EvaluateReceiveQualification(uint param_1,byte param_2,uint param_3)

{
  bool bVar1;
  uint uVar2;
  int iVar3;
  ushort uVar4;
  char cVar5;
  byte bVar6;
  byte bVar7;
  int iVar8;
  int iVar9;
  uint uVar10;
  int iVar11;
  ushort *puVar12;
  int iVar13;
  uint uVar14;
  int iVar15;
  int iVar16;
  undefined4 uVar17;
  uint uVar18;
  byte bStack_38;
  byte local_34;
  
  uVar2 = (uint)param_2;
  uVar18 = 0;
  if (uVar2 == 0x36) {
    uVar14 = 0;
  }
  else if (uVar2 == 0x37) {
    uVar14 = 1;
  }
  else {
    uVar14 = (int)DAT_0001a5e0;
    if (uVar2 == 0x38) {
      uVar14 = 2;
    }
  }
  uVar10 = uVar14 & 0xff;
  if (uVar10 != (int)DAT_0001a5e0) {
    puVar12 = (ushort *)(int)DAT_0001a6f0;
    iVar16 = (uVar14 & 0xff) * 0x12;
    iVar3 = (uVar14 & 0xff) * 0x48;
    iVar15 = (uVar14 & 0xff) * 0x24;
    uVar4 = (*(code *)PTR_FUN_0001a700)();
    uVar2 = param_1 & 0xff;
    if (uVar2 == 0) {
      uVar18 = 0;
      do {
        iVar11 = (int)DAT_0001a6f6;
        uVar2 = uVar18 & 0xff;
        iVar8 = (int)DAT_0001a6f8;
        *(undefined1 *)(DAT_0001a6f2 + iVar16 + uVar2) = 2;
        iVar13 = (uVar18 & 0xff) * 4;
        iVar9 = (uVar18 & 0xff) * 2;
        *(undefined4 *)(iVar13 + iVar3 + DAT_0001a6f4) = 0;
        *(undefined2 *)(iVar11 + iVar15 + iVar9) = 0;
        uVar18 = uVar18 + 1;
        iVar11 = (int)DAT_0001a6fa;
        *(undefined1 *)(uVar2 + iVar8 + iVar16) = 2;
        iVar8 = (int)DAT_0001a6fc;
        *(undefined4 *)(iVar13 + iVar3 + iVar11) = 0;
        uVar2 = uVar18 & 0xff;
        *(undefined2 *)(iVar9 + iVar8 + iVar15) = 0;
      } while (uVar2 < 0x12);
    }
    else if (uVar2 == 0x14) {
      iVar8 = (int)DAT_0001a6f6;
      *(undefined1 *)(DAT_0001a6f2 + iVar16 + (param_3 & 0xff)) = 2;
      iVar11 = (param_3 & 0xff) * 2;
      iVar3 = (int)DAT_0001a6f8;
      *(undefined2 *)(iVar8 + iVar15 + iVar11) = 0;
      iVar8 = (int)DAT_0001a6fc;
      *(undefined1 *)((param_3 & 0xff) + iVar3 + iVar16) = 2;
      *(undefined2 *)(iVar11 + iVar8 + iVar15) = 0;
      *puVar12 = *puVar12 & ~uVar4;
    }
    else if (uVar2 == 0x15) {
      *puVar12 = *puVar12 | uVar4;
    }
    else if (uVar2 == 1) {
      local_34 = 0;
      uVar17 = 0;
      cVar5 = (*(code *)PTR_FUN_0001a854)();
      if ((cVar5 == '\0') && (*PTR_Diagnostic_CommunicationAdmission_0001a858 == '\x01')) {
        iVar11 = (int)DAT_0001a848;
        uVar2 = 0;
        iVar8 = (int)DAT_0001a84a;
        local_34 = 1;
        bVar7 = 0;
        bVar1 = false;
        iVar9 = (int)DAT_0001a84c;
        do {
          if (((((byte)PTR_CAN_RecordConfiguration_0001a85c[(uVar2 & 0xff) * 0x1c + 0xd] == uVar10)
               && (PTR_CAN_RecordConfiguration_0001a85c[(uVar2 & 0xff) * 0x1c + 0x14] == '\x01')) &&
              (bVar6 = CAN_UpdateQualificationTimer
                                 (1,1,(uVar2 & 0xff) + iVar9 + iVar16,
                                  (uVar2 & 0xff) * 4 + iVar3 + iVar8,
                                  (uVar2 & 0xff) * 2 + iVar11 + iVar15,(int)(char)param_2,0,uVar2),
              bVar6 != 0)) &&
             (bVar7 = bVar7 | bVar6,
             (ushort)(byte)PTR_DAT_0001a860[(uVar2 & 0xff) * 0x1c] <=
             *(ushort *)((uVar2 & 0xff) * 2 + iVar11 + iVar15))) {
            bVar1 = true;
          }
          uVar2 = uVar2 + 1;
        } while ((uVar2 & 0xff) < 0x12);
        if ((bVar7 != 0) && (local_34 = 3, bVar1)) {
          local_34 = 7;
        }
        uVar17 = 1;
        iVar8 = (int)DAT_0001a84e;
        bStack_38 = 0;
        iVar11 = (int)DAT_0001a850;
        iVar9 = (int)DAT_0001a852;
        do {
          if ((((byte)PTR_CAN_RecordConfiguration_0001a85c[(uVar18 & 0xff) * 0x1c + 0xd] == uVar10)
              && (PTR_CAN_RecordConfiguration_0001a85c[(uVar18 & 0xff) * 0x1c + 0x14] == '\x01')) &&
             (bVar7 = CAN_UpdateQualificationTimer
                                (1,1,(uVar18 & 0xff) + iVar9 + iVar16,
                                 (uVar18 & 0xff) * 4 + iVar3 + iVar11,
                                 (uVar18 & 0xff) * 2 + iVar8 + iVar15,(int)(char)param_2,1,uVar18),
             bVar7 != 0)) {
            bStack_38 = bStack_38 | bVar7;
          }
          uVar18 = uVar18 + 1;
        } while ((uVar18 & 0xff) < 0x12);
        if (bStack_38 == 0) {
          uVar17 = 3;
          if ((PTR_DAT_0001a99c[param_2] & 2) != 0) {
            local_34 = local_34 | 0x80;
          }
          uVar2 = (*(code *)PTR_FUN_0001a9a0)((int)(char)param_2);
          if (((PTR_DAT_0001a99c[param_2] & 4) != 0) && ((uVar2 & 1) == 1)) {
            local_34 = local_34 | 0x80;
          }
        }
      }
      else {
        bVar7 = 0;
        do {
          uVar2 = (uint)bVar7;
          iVar8 = (int)DAT_0001a992;
          uVar14 = (uint)bVar7;
          iVar11 = (int)DAT_0001a98e;
          uVar18 = (uint)bVar7;
          *(undefined1 *)(DAT_0001a98c + iVar16 + uVar14) = 2;
          iVar9 = (int)DAT_0001a990;
          *(undefined4 *)(uVar2 * 4 + iVar3 + iVar11) = 0;
          iVar11 = (int)DAT_0001a996;
          bVar7 = bVar7 + 1;
          *(undefined2 *)(iVar9 + iVar15 + uVar18 * 2) = 0;
          *(undefined1 *)(uVar14 + iVar8 + iVar16) = 2;
          *(undefined4 *)(uVar2 * 4 + iVar3 + DAT_0001a994) = 0;
          *(undefined2 *)(uVar18 * 2 + iVar11 + iVar15) = 0;
        } while (bVar7 < 0x12);
      }
      cVar5 = PTR_DAT_0001a9a4[(uint)param_2 * 0x10];
      (*(code *)PTR_Diagnostic_StoreGroupStatus_0001a9a8)((int)(char)param_2,(int)(char)local_34);
      uVar2 = (*(code *)PTR_Diagnostic_StoreMappedStatus_0001a9ac)((int)cVar5,uVar17);
      return uVar2;
    }
  }
  return uVar2;
}

