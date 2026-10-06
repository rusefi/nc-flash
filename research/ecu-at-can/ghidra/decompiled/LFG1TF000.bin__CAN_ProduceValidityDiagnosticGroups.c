/* Ghidra analysis output; verify against original SH instructions. */

/* Table5F198 maps8816->3A,AC7A->3B,880A->3C,880E->3D,8812->3E. A939==1 andA977/A978mask08 clear
   admit.2048 producer cases and timedCAN201 invalid/recovery lifecycles; see can201-invalid.txt and
   can215-invalid.txt. */

void CAN_ProduceValidityDiagnosticGroups(void)

{
  byte bVar2;
  uint uVar1;
  undefined4 *puVar3;
  undefined4 uVar4;
  undefined4 *puVar5;
  undefined *puVar6;
  uint uVar7;
  undefined *puStack_28;
  
  puVar6 = PTR_DAT_000584e4;
  *(char *)(int)DAT_000584dc = -(((PTR_DAT_000584e4[0x1f] & 8) == 0) + -1);
  *(char *)(int)DAT_000584de = -(((puVar6[0x20] & 8) == 0) + -1);
  CAN_CombineTwoValidityInputs();
  puStack_28 = PTR_CAN_ValidityDiagnosticTable_000584e8;
  puVar3 = (undefined4 *)(PTR_CAN_ValidityDiagnosticTable_000584e8 + 0x28);
  puVar5 = (undefined4 *)PTR_CAN_ValidityDiagnosticTable_000584e8;
  puVar6 = PTR_CAN_ValidityDiagnosticTable_000584e8;
  do {
    uVar7 = 0;
    uVar4 = 0;
    if (((*PTR_DAT_000584ec == '\x01') && (*(char *)(int)DAT_000584dc == '\0')) &&
       (*(char *)(int)DAT_000584de == '\0')) {
      uVar7 = 1;
      uVar4 = 1;
      if (*(char *)*puVar5 == '\x01') {
        uVar7 = 3;
      }
      else if (*(char *)*puVar5 == '\x02') {
        uVar4 = 3;
        bVar2 = (*(code *)PTR_FUN_000584f0)((int)(char)puVar6[4]);
        uVar1 = (*(code *)PTR_FUN_000584f4)((int)(char)puVar6[4]);
        if ((bVar2 & 2) == 2) {
          uVar7 = (uint)DAT_000584e0;
        }
        if (((bVar2 & 4) == 4) && ((uVar1 & 1) == 1)) {
          uVar7 = uVar7 | (int)DAT_000584e2;
        }
      }
    }
    bVar2 = puStack_28[4];
    (*(code *)PTR_Diagnostic_StoreGroupStatus_000584f8)((int)(char)bVar2,uVar7);
    (*(code *)PTR_Diagnostic_StoreMappedStatus_00058500)
              ((int)(char)PTR_DAT_000584fc[(uint)bVar2 * 0x10],uVar4);
    puVar5 = puVar5 + 2;
    puStack_28 = puStack_28 + 8;
    puVar6 = puVar6 + 8;
  } while (puVar5 < puVar3);
  return;
}

