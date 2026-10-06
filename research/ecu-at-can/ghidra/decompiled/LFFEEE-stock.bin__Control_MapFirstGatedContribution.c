/* Ghidra analysis output; verify against original SH instructions. */

/* 80E4=A3670(6D28)if7012exact1,elseA367C. Raw2 selectsothermap. */

void Control_MapFirstGatedContribution(void)

{
  char cVar1;
  undefined *puVar2;
  undefined4 uVar3;
  
  cVar1 = (*(code *)PTR_FUN_0005933c)(PTR_DAT_0005935c);
  puVar2 = PTR_Control_FirstContributionOtherModeDescriptor_00059364;
  if (cVar1 == '\x01') {
    puVar2 = PTR_Control_FirstContributionModeOneDescriptor_00059360;
  }
  uVar3 = (*(code *)PTR_FUN_0005936c)(PTR_DAT_00059368);
  uVar3 = (*(code *)PTR_Lookup_FloatCurve_00059370)(uVar3,puVar2);
  *(undefined4 *)PTR_Control_FirstGatedContributionMap_0005934c = uVar3;
  return;
}

