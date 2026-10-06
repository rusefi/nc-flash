/* Ghidra analysis output; verify against original SH instructions. */

/* Two5-knot curves at76474/764CC familygroups,axisrecord+14,eachlookup>>2; code/operation/95AEbit0
   selectfamily. Executed through4CD18. See tcu-request-dispatch.txt. */

void SparkRequest_ActivationOffsets(uint *param_1,uint *param_2,int param_3)

{
  char cVar1;
  short sVar2;
  uint uVar3;
  undefined *puVar4;
  undefined *puVar5;
  
  sVar2 = *(short *)(param_3 + 0xe);
  cVar1 = *(char *)(param_3 + 1);
  puVar4 = PTR_SparkRequest_ActivationOffsetCurves_44__0004d81c;
  puVar5 = PTR_SparkRequest_ActivationOffsetCurves_132__0004d820;
  if ((((cVar1 != '\t') &&
       (puVar4 = PTR_SparkRequest_ActivationOffsetCurves_33__0004d824,
       puVar5 = PTR_SparkRequest_ActivationOffsetCurves_121__0004d828, cVar1 != '\b')) &&
      (cVar1 != '\v')) &&
     (puVar4 = PTR_SparkRequest_ActivationOffsetCurves_77__0004d82c,
     puVar5 = PTR_SparkRequest_ActivationOffsetCurves_165__0004d830, cVar1 != '\n')) {
    if (cVar1 == '\a') {
      puVar4 = PTR_SparkRequest_ActivationOffsetCurves_22__0004d834;
      puVar5 = PTR_SparkRequest_ActivationOffsetCurves_110__0004d838;
      if ((*PTR_DAT_0004d83c & 1) == 1) {
        puVar4 = PTR_SparkRequest_ActivationOffsetCurves_55__0004d814;
        puVar5 = PTR_SparkRequest_ActivationOffsetCurves_143__0004d818;
      }
    }
    else {
      puVar4 = PTR_SparkRequest_ActivationOffsetCurves_11__0004d840;
      puVar5 = PTR_SparkRequest_ActivationOffsetCurves_99__0004d844;
      if (cVar1 != '\x06') {
        puVar4 = PTR_SparkRequest_ActivationOffsetCurves_0004d848;
        puVar5 = PTR_SparkRequest_ActivationOffsetCurves_88__0004d84c;
      }
    }
  }
  if (*(char *)(param_3 + 8) == '\x18') {
    puVar4 = PTR_SparkRequest_ActivationOffsetCurves_66__0004d850;
    puVar5 = PTR_SparkRequest_ActivationOffsetCurves_154__0004d854;
  }
  if (*(char *)(param_3 + 8) == '\x17') {
    puVar4 = PTR_SparkRequest_ActivationOffsetCurves_55__0004d814;
    puVar5 = PTR_SparkRequest_ActivationOffsetCurves_143__0004d818;
  }
  uVar3 = (*(code *)PTR_Lookup_ByteCurveToFixedPoint_0004d858)((int)sVar2,puVar4);
  puVar4 = PTR_Lookup_ByteCurveToFixedPoint_0004d858;
  *param_1 = (uVar3 & 0xffff) >> 2;
  uVar3 = (*(code *)puVar4)((int)sVar2,puVar5);
  *param_2 = (uVar3 & 0xffff) >> 2;
  return;
}

