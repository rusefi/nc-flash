/* Ghidra analysis output; verify against original SH instructions. */

/* Phase gated; cut array6E34+cyl -> bit80 in78CF+cyl. Calls42EA8. */

void UpdateCylinderCutStatus(void)

{
  char cVar1;
  char cVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined *puVar5;
  undefined4 uVar6;
  byte bVar7;
  byte *pbVar8;
  
  uVar6 = (*(code *)PTR_FUN_0004d800)(0x10);
  puVar5 = PTR_DAT_0004d814;
  puVar4 = PTR_DAT_0004d810;
  puVar3 = PTR_CylinderCutStatusBase_0004d80c;
  bVar7 = 1;
  cVar1 = *PTR_DAT_0004d804;
  cVar2 = *PTR_DAT_0004d808;
  do {
    if (cVar1 == puVar5[(uint)bVar7 * 4 + 3]) {
      pbVar8 = puVar3 + bVar7;
      if ((((((puVar4[bVar7] & 0x40) == 0) && (PTR_DAT_0004d818[bVar7] != '\x01')) &&
           (cVar2 != '\x01')) && ((*PTR_DAT_0004d81c != '\x01' || ((bVar7 != 1 && (bVar7 != 4))))))
         && (PTR_DAT_0004d820[bVar7] != '\x01')) {
        *pbVar8 = *pbVar8 & 0x7f;
      }
      else {
        *pbVar8 = *pbVar8 | 0x80;
      }
    }
    bVar7 = bVar7 + 1;
  } while (bVar7 < 5);
  (*(code *)PTR_AggregateCylinderCutMask_0004d9b0)();
  (*(code *)PTR_FUN_0004d9b4)(uVar6);
  return;
}

