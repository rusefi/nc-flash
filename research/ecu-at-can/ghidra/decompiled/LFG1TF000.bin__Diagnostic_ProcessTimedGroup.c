/* Ghidra analysis output; verify against original SH instructions. */

/* Group15 executes five 2000-tick qualification intervals before stored0707; absolute units and
   recovery open. */

void Diagnostic_ProcessTimedGroup(uint param_1)

{
  byte bVar1;
  byte bVar2;
  bool bVar3;
  bool bVar4;
  char cVar5;
  byte *pbVar6;
  
  pbVar6 = PTR_DAT_000567fc + (param_1 & 0xff);
  bVar2 = *(byte *)((param_1 & 0xff) + (int)DAT_000567f8);
  bVar1 = *pbVar6;
  bVar3 = (bVar1 & 1) == 0;
  bVar4 = (bVar1 & 4) == 0;
  cVar5 = (*(code *)PTR_FUN_00056800)(param_1);
  if ((bVar4) ||
     ((PTR_Diagnostic_GroupConfiguration_00056804[(param_1 & 0xff) * 0x10 + 6] & 0x10) == 0x10)) {
    if ((bVar2 & 2) == 0) {
      if ((!bVar3) || ((bVar1 & 0x40) != 0)) {
        *pbVar6 = *pbVar6 & 0xfe;
        FUN_00056896(param_1);
        return;
      }
    }
    else {
      *pbVar6 = *pbVar6 & 0xbf;
      if (bVar3) {
        if ((bVar4) || (cVar5 == '\x01')) {
          FUN_000567c0(param_1);
        }
        *pbVar6 = *pbVar6 | 1;
      }
      else if ((bVar4) || (cVar5 == '\x01')) {
        FUN_00056814(param_1);
        return;
      }
    }
  }
  return;
}

