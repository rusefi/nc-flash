/* Ghidra analysis output; verify against original SH instructions. */

/* 7234exact1 increases80EC bystock~.007 withuppercap1;otherrawvalues decreaseby~.007
   withlowerfloor0. FiniteRTZoracle; bothendpoints reached inretainedlife. */

undefined4 Control_UpdateContributionBlendWeight(void)

{
  char cVar2;
  undefined4 uVar1;
  undefined4 extraout_fr0;
  undefined4 extraout_fr0_00;
  undefined4 uVar3;
  float fVar4;
  
  fVar4 = *(float *)PTR_Control_ContributionBlendWeight_00059344;
  cVar2 = (*(code *)PTR_FUN_0005933c)(PTR_DAT_0005937c);
  if (cVar2 == '\x01') {
    uVar1 = (*(code *)PTR_FUN_00059384)(*(float *)PTR_DAT_00059380 + fVar4,0x3f800000);
    uVar3 = extraout_fr0;
  }
  else {
    uVar1 = (*(code *)PTR_FUN_0005938c)(fVar4 - *(float *)PTR_DAT_00059388,0);
    uVar3 = extraout_fr0_00;
  }
  *(undefined4 *)PTR_Control_ContributionBlendWeight_00059344 = uVar3;
  return uVar1;
}

