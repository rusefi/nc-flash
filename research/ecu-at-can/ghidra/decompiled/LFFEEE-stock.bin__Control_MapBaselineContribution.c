/* Ghidra analysis output; verify against original SH instructions. */

/* 80C8=A365C(6D38,6D30);original14x3floatmap andbilinear helper executed. Allknots/midpoints
   andclamps tested. */

void Control_MapBaselineContribution(void)

{
  undefined4 uVar1;
  undefined4 uVar2;
  
  uVar1 = (*(code *)PTR_FUN_00059120)(PTR_DAT_0005911c);
  uVar2 = (*(code *)PTR_FUN_00059120)(PTR_DAT_00059124);
  uVar1 = (*(code *)PTR_Lookup_FloatMap2D_0005912c)
                    (uVar2,uVar1,PTR_Control_BaselineContributionDescriptor_00059128);
  *(undefined4 *)PTR_Control_TwoInputBaselineMap_00059114 = uVar1;
  return;
}

