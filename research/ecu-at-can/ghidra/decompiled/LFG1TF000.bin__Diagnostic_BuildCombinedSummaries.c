/* Ghidra analysis output; verify against original SH instructions. */

/* Builds A98B..A994 from table5FCBC. A98E combines A977/A978/A97C (groups35/36/3A); active02/04
   sets08, history10 alone does not.146 mapping and512 paired cases. */

void Diagnostic_BuildCombinedSummaries(void)

{
  undefined *puVar1;
  undefined *puVar2;
  byte *pbVar3;
  byte bVar4;
  int iVar5;
  byte *pbVar6;
  undefined *puVar7;
  undefined *puVar8;
  byte *pbVar9;
  byte local_24 [8];
  
  puVar2 = PTR_DAT_00057370;
  puVar1 = PTR_FUN_0005736c;
  pbVar6 = PTR_DAT_00057368 + 0x28;
  puVar7 = PTR_DAT_00057364;
  puVar8 = PTR_DAT_00057368;
  pbVar9 = PTR_DAT_00057368;
  do {
    local_24[0] = 1;
    iVar5 = 0;
    bVar4 = *pbVar9;
    while (bVar4 != 0) {
      pbVar3 = puVar2 + bVar4;
      if ((*pbVar3 & 4) != 0) {
        local_24[0] = local_24[0] & 0xfe | 0xc;
      }
      if ((*pbVar3 & 2) != 0) {
        local_24[0] = local_24[0] & 0xfe | 10;
      }
      iVar5 = iVar5 + 1;
      if ((*pbVar3 & 0x10) != 0) {
        local_24[0] = local_24[0] | 0x10;
      }
      bVar4 = puVar8[iVar5];
    }
    (*(code *)puVar1)(puVar7,local_24,1);
    puVar7 = puVar7 + 1;
    pbVar9 = pbVar9 + 4;
    puVar8 = puVar8 + 4;
  } while (pbVar9 < pbVar6);
  return;
}

