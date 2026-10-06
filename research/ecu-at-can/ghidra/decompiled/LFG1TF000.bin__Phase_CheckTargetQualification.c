/* Ghidra analysis output; verify against original SH instructions. */

/* WARNING: Removing unreachable block (ram,0x0003254c) */
/* 92C6 bits1/4 return-1 and preserve bounds/counters/flags. Otherwise target-reference +/-128
   ->9700/9704; ascending32614 or descending327B0 qualifies return2. Ascending2560 all-byte
   inhibit/index cases plus retained manager trace; tcu-ascending-phase.txt. */

undefined4 Phase_CheckTargetQualification(undefined4 param_1,uint param_2)

{
  undefined *puVar1;
  short sVar2;
  char cVar3;
  char cVar4;
  char cVar5;
  int iVar6;
  int iVar7;
  undefined4 uVar8;
  short sStack_2c;
  
  uVar8 = 0xffffffff;
  if (((*PTR_ApplicationFaultFlags92C6_00032538 & 0x10) == 0) &&
     ((*PTR_ApplicationFaultFlags92C6_00032538 & 2) == 0)) {
    iVar7 = 1;
    iVar6 = *(int *)(PTR_Phase_ProducedReferenceWords_00032534 +
                    (uint)(byte)PTR_DAT_00032544[param_2 & 0xffff] * 4);
    sVar2 = (*(code *)PTR_FUN_00032600)();
    *(int *)(int)DAT_000325f6 = sVar2 + iVar6;
    if (iVar7 == 0) {
      sStack_2c = (short)((uint)DAT_000325fc >> 0x10);
    }
    else {
      sStack_2c = (short)((uint)DAT_00032604 >> 0x10);
    }
    sVar2 = (*(code *)PTR_FUN_00032600)();
    puVar1 = PTR_Phase_ClassifyDirection_00032608;
    *(int *)(int)DAT_000325f8 = iVar6 - sVar2;
    cVar3 = (*(code *)puVar1)(param_2);
    cVar4 = '\0';
    cVar5 = '\0';
    if (cVar3 == '\0') {
      cVar4 = Phase_QualifyAscendingTarget(0,param_2,(int)sStack_2c);
    }
    else {
      *(byte *)(int)DAT_000325fa = *(byte *)(int)DAT_000325fa & 0xfd;
      cVar5 = Phase_QualifyDescendingTarget(0,param_2,(int)sStack_2c);
    }
    if ((cVar4 == '\x01') || (cVar5 == '\x01')) {
      uVar8 = 2;
    }
  }
  return uVar8;
}

