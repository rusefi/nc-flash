/* Ghidra analysis output; verify against original SH instructions. */

/* 8130 mode7012exact1 A36D0 elseA36DC. Rising812Bexact1 from8135zero
   captures8124/reloads8129stock0;otherwisecountdownthendecay1or.00075. Publishraw8135. */

uint Control_ProduceSecondNormalizedTerm(void)

{
  char cVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  char cVar6;
  uint uVar5;
  float *pfVar7;
  undefined4 uVar8;
  undefined4 extraout_fr0;
  float fVar9;
  
  puVar2 = PTR_Control_SecondContributionTarget_000599b4;
  cVar1 = *PTR_Control_SecondContributionGate_000599ac;
  cVar6 = (*(code *)PTR_FUN_000599bc)(PTR_DAT_000599b8);
  if (cVar6 == '\x01') {
    uVar8 = (*(code *)PTR_Lookup_FloatCurve_00059994)
                      (*(undefined4 *)PTR_Control_FilteredContributionInput_0005998c,
                       PTR_Model_FloatCurve_ARRAY_000599c0);
    pfVar7 = (float *)PTR_DAT_000599c4;
    *(undefined4 *)puVar2 = uVar8;
  }
  else {
    uVar8 = (*(code *)PTR_Lookup_FloatCurve_00059994)
                      (*(undefined4 *)PTR_Control_FilteredContributionInput_0005998c,
                       PTR_Model_FloatCurve_ARRAY_000599c8);
    *(undefined4 *)puVar2 = uVar8;
    pfVar7 = (float *)PTR_DAT_000599cc;
  }
  puVar4 = PTR_Control_SecondContributionCountdown_000599d4;
  puVar3 = PTR_Control_SecondNormalizedTerm_000599d0;
  fVar9 = *pfVar7;
  if ((*PTR_Control_PreviousSecondContributionGate_000599d8 == '\0') && (cVar1 == '\x01')) {
    *(undefined4 *)PTR_Control_SecondNormalizedTerm_000599d0 = *(undefined4 *)puVar2;
    *puVar4 = *PTR_DAT_000599dc;
    uVar5 = 1;
  }
  else {
    uVar5 = (uint)(byte)*PTR_Control_SecondContributionCountdown_000599d4;
    if (uVar5 != 0) {
      *PTR_Control_SecondContributionCountdown_000599d4 =
           *PTR_Control_SecondContributionCountdown_000599d4 + (char)DAT_00059a16;
    }
    if (*puVar4 == '\0') {
      uVar5 = (*(code *)PTR_FUN_00059a18)(*(float *)puVar3 - fVar9,0);
      *(undefined4 *)puVar3 = extraout_fr0;
    }
  }
  *PTR_Control_PreviousSecondContributionGate_00059a1c = cVar1;
  return uVar5;
}

