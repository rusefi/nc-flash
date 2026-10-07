/* Ghidra analysis output; verify against original SH instructions. */

/* 6D54=A261C(7BB8);stockC89A0zero:protected6D4C=RTZ(6DC4-RTZ(RTZ(6D54*RTZ(6D40+273))/293)).
   Fulloriginalbodyexecuted. */

void Control_MapRatioEnvironmentDifference(void)

{
  float fVar1;
  float fVar2;
  
  fVar1 = (float)(*(code *)PTR_Lookup_FloatCurve_0003a018)
                           (*(undefined4 *)PTR_Control_RatioContributionSum_0003a010,
                            PTR_Control_ContributionMapDescriptor_0003a014);
  *(float *)PTR_Control_IntermediateContributionMap_0003a01c = fVar1;
  fVar2 = (float)(*(code *)PTR_FUN_0003a024)(PTR_Control_RawSecondPublished_0003a020);
  fVar2 = (fVar1 * (fVar2 + DAT_0003a028)) / DAT_0003a02c;
  fVar1 = DAT_0003a034;
  if (*PTR_DAT_0003a030 == '\0') {
    fVar1 = (float)(*(code *)PTR_FUN_0003a024)(PTR_DAT_0003a038);
  }
  (*(code *)PTR_FUN_0003a040)(fVar1 - fVar2,PTR_Control_ProtectedMapDifference_0003a03c);
  return;
}

