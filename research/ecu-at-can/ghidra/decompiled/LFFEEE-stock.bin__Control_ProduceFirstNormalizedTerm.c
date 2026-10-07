/* Ghidra analysis output; verify against original SH instructions. */

/* 811C=A36C4(8120) while8128nonzero,elsemax(old-.001,0).405cases;originallookup. */

undefined4 Control_ProduceFirstNormalizedTerm(void)

{
  undefined *puVar1;
  undefined4 uVar2;
  undefined4 extraout_fr0;
  undefined4 extraout_fr0_00;
  undefined4 uVar3;
  
  puVar1 = PTR_Control_FirstNormalizedTerm_00059984;
  if (*PTR_Control_FirstContributionCountdown_00059988 == '\0') {
    uVar2 = (*(code *)PTR_FUN_0005999c)
                      (*(float *)PTR_Control_FirstNormalizedTerm_00059984 -
                       *(float *)PTR_DAT_00059998,0);
    uVar3 = extraout_fr0_00;
  }
  else {
    uVar2 = (*(code *)PTR_Lookup_FloatCurve_00059994)
                      (*(undefined4 *)PTR_Control_FilteredContributionInput_0005998c,
                       PTR_Model_FloatCurve_ARRAY_00059990);
    uVar3 = extraout_fr0;
  }
  *(undefined4 *)puVar1 = uVar3;
  return uVar2;
}

