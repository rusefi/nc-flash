/* Ghidra analysis output; verify against original SH instructions. */

/* Executed tail branch8FB52 withr6=0; groups43/44 reports/cache verified. No generic stored-DTC
   lifecycle claim. */

uint Diagnostic_ReportUntimedGroup(uint param_1,char param_2)

{
  short sVar1;
  short sVar2;
  bool bVar3;
  char cVar7;
  undefined4 uVar4;
  uint uVar5;
  undefined4 uVar6;
  
  sVar1 = *(short *)PTR_DAT_0008fc50;
  sVar2 = *(short *)(PTR_LAB_0008fc54 + (param_1 & 0xffff) * 2);
  cVar7 = (*(code *)PTR_FUN_0008fc5c)(PTR_DAT_0008fc58);
  if ((cVar7 == '\x01') || (*PTR_DAT_0008fc60 == '\x01')) {
    bVar3 = true;
  }
  else {
    bVar3 = false;
  }
  if (bVar3) {
    uVar4 = 0;
  }
  else {
    uVar4 = Diagnostic_CacheGroupMode(param_1,(int)param_2);
  }
  uVar5 = (uint)*DAT_0008fc40;
  if (uVar5 == 1) {
    uVar5 = (*(code *)PTR_Diagnostic_CheckRuntimeMaskAbsent_0008fc64)((int)sVar2,(int)sVar1);
    uVar5 = uVar5 & 0xff;
    if (uVar5 == 0) {
      if (*PTR_DAT_0008fc68 != '\0') {
        uVar6 = (*(code *)PTR_FUN_0008fc70)(0x10);
        if (*PTR_DAT_0008fc74 == '\0') {
          FUN_0008fe4e(param_1,uVar4,0);
        }
        uVar5 = (*(code *)PTR_FUN_0008fc78)(uVar6);
        return uVar5;
      }
      uVar5 = (*(code *)PTR_Diagnostic_CheckEnableMaskAbsent_0008fc6c)((int)sVar2,1);
      uVar5 = uVar5 & 0xff;
      if ((uVar5 == 0) && (!bVar3)) {
        uVar5 = FUN_0008fcb8(param_1,uVar4,0);
        return uVar5;
      }
    }
  }
  return uVar5;
}

