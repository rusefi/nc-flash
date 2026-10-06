/* Ghidra analysis output; verify against original SH instructions. */

/* 80E8=A3688(6D28)if7012exact1,elseA3694. Executed stockcurves. */

void Control_MapSecondGatedContribution(void)

{
  char cVar1;
  undefined *puVar2;
  undefined4 uVar3;
  
  cVar1 = (*(code *)PTR_FUN_0005933c)(PTR_DAT_0005935c);
  puVar2 = PTR_Control_SecondContributionOtherModeDescriptor_00059378;
  if (cVar1 == '\x01') {
    puVar2 = PTR_Control_SecondContributionModeOneDescriptor_00059374;
  }
  uVar3 = (*(code *)PTR_FUN_0005936c)(PTR_DAT_00059368);
  uVar3 = (*(code *)PTR_Lookup_FloatCurve_00059370)(uVar3,puVar2);
  *(undefined4 *)PTR_Control_SecondGatedContributionMap_00059350 = uVar3;
  return;
}

