/* Ghidra analysis output; verify against original SH instructions. */

/* ConsumesA736+group bits04/02 andA6EC+group state. Group36 qualification reaches storedC100
   andA99B. Healthy recovery clears active04 subject to56A4A/80A4. */

void Diagnostic_ProcessQualifiedGroup(uint param_1)

{
  byte bVar1;
  byte bVar2;
  bool bVar3;
  bool bVar4;
  undefined *puVar5;
  char cVar6;
  byte *pbVar7;
  int iVar8;
  
  bVar1 = *(byte *)((param_1 & 0xff) + DAT_00056a08);
  bVar2 = *(byte *)((param_1 & 0xff) + (int)sRam00056a06);
  bVar3 = (bVar1 & 4) == 0;
  bVar4 = (bVar1 & 2) == 0;
  cVar6 = (*pcRam00056a0c)(param_1);
  if ((bVar3) || ((*(byte *)((param_1 & 0xff) * 0x10 + iRam00056a10 + 6) & 0x10) == 0x10)) {
    if ((bVar2 & 4) == 0) {
      if ((bVar2 & 2) == 0) {
        if (((!bVar4) || (!bVar3)) &&
           (cVar6 = Diagnostic_CheckActiveRecoveryPermission(param_1), cVar6 == '\x01')) {
          iVar8 = 0;
          goto code_r0x000569ea;
        }
      }
      else if ((bVar3) && (bVar4)) {
        iVar8 = 2;
code_r0x000569ea:
        pbVar7 = (byte *)((param_1 & 0xff) + DAT_00056a08);
        if (iVar8 == 2) {
          *pbVar7 = *pbVar7 | 2;
        }
        else if (iVar8 == 4) {
          *pbVar7 = *pbVar7 | 4;
          puVar5 = PTR_Diagnostic_RecordQualifiedGroup_00056ac0;
          *pbVar7 = *pbVar7 & 0xfd;
          (*(code *)puVar5)(param_1);
          FUN_00056a86(param_1);
        }
        else if (iVar8 == 0) {
          *pbVar7 = *pbVar7 & 0xf9;
          *pbVar7 = *pbVar7 & 0x7f;
        }
                    /* WARNING: Could not recover jumptable at 0x00056a46. Too many branches */
                    /* WARNING: Treating indirect jump as call */
        (*(code *)PTR_Diagnostic_UpdateActiveAggregate_00056ac4)();
        return;
      }
    }
    else if ((bVar3) || (cVar6 == '\x01')) {
      Diagnostic_UpdateActiveGroup(param_1,4);
    }
  }
  return;
}

