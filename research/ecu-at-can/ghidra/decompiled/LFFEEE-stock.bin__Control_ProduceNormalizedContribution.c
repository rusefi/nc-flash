/* Ghidra analysis output; verify against original SH instructions. */

/* 8118=(812C+max811C,8124)/stockscaled7020 whenabsdivisor>2^-17;otherwisehold8118.
   Alwaysrefresh812C via7012exact1 selectedA36AC/B8.
   control-normalized-contribution.txt;10034direct+12callersegments/320cycles. */

uint Control_ProduceNormalizedContribution(void)

{
  undefined *puVar1;
  char cVar3;
  uint uVar2;
  undefined4 uVar4;
  float extraout_fr0;
  float fVar5;
  
  puVar1 = PTR_Control_NormalizedMappedTerm_0005982c;
  cVar3 = (*(code *)PTR_FUN_00059834)(PTR_DAT_00059830);
  if (cVar3 == '\x01') {
    uVar4 = (*(code *)PTR_FUN_0005983c)(PTR_Control_PublishedNormalizedMapInput_00059838);
    uVar4 = (*(code *)PTR_Lookup_FloatCurve_00059844)(uVar4,PTR_Model_FloatCurve_ARRAY_00059840);
  }
  else {
    uVar4 = (*(code *)PTR_FUN_0005983c)(PTR_Control_PublishedNormalizedMapInput_00059838);
    uVar4 = (*(code *)PTR_Lookup_FloatCurve_00059844)(uVar4,PTR_Model_FloatCurve_ARRAY_00059848);
  }
  *(undefined4 *)puVar1 = uVar4;
  fVar5 = (((*(float *)PTR_DAT_00059850 * *(float *)PTR_DAT_0005984c) / 2.0) *
          *(float *)PTR_DAT_00059854) / DAT_00059858;
  uVar2 = (*(code *)PTR_FUN_00059860)(fVar5,0,DAT_0005985c);
  if ((uVar2 & 0xff) != 0) {
    uVar2 = (*(code *)PTR_FUN_0005986c)
                      (*(undefined4 *)PTR_Control_FirstNormalizedTerm_00059868,
                       *(undefined4 *)PTR_Control_SecondNormalizedTerm_00059864);
    *(float *)PTR_Control_NormalizedContribution_00059870 =
         (*(float *)puVar1 + extraout_fr0) / fVar5;
  }
  return uVar2;
}

