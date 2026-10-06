/* Ghidra analysis output; verify against original SH instructions. */

/* Selects4-knot curve bycode/operation/95AEbit0,axis4*clamp(s16(80EA),0,3FFF), lookup>>8. Executed
   through activationpredicate. See tcu-request-dispatch.txt. */

uint SparkRequest_ActivationDerivativeFactor(int param_1)

{
  char cVar1;
  undefined4 uVar2;
  uint uVar3;
  undefined *puVar4;
  
  cVar1 = *(char *)(param_1 + 1);
  puVar4 = PTR_SparkRequest_ActivationFactorCurves_36__0004d464;
  if ((((cVar1 != '\t') &&
       (puVar4 = PTR_SparkRequest_ActivationFactorCurves_27__0004d468, cVar1 != '\b')) &&
      (cVar1 != '\v')) &&
     (puVar4 = PTR_SparkRequest_ActivationFactorCurves_63__0004d46c, cVar1 != '\n')) {
    if (cVar1 == '\a') {
      puVar4 = PTR_SparkRequest_ActivationFactorCurves_18__0004d470;
      if ((*PTR_DAT_0004d474 & 1) == 1) {
        puVar4 = PTR_SparkRequest_ActivationFactorCurves_45__0004d460;
      }
    }
    else {
      puVar4 = PTR_SparkRequest_ActivationFactorCurves_9__0004d478;
      if (cVar1 != '\x06') {
        puVar4 = PTR_SparkRequest_ActivationFactorCurves_0004d47c;
      }
    }
  }
  if (*(char *)(param_1 + 8) == '\x18') {
    puVar4 = PTR_SparkRequest_ActivationFactorCurves_54__0004d480;
  }
  if (*(char *)(param_1 + 8) == '\x17') {
    puVar4 = PTR_SparkRequest_ActivationFactorCurves_45__0004d460;
  }
  uVar2 = (*(code *)PTR_Measurement_ClampAndScaleCurveAxis_0004d484)((int)DAT_ffff80ea);
  uVar3 = (*(code *)PTR_Lookup_ByteCurveToFixedPoint_0004d488)(uVar2,puVar4);
  return (uVar3 & 0xffff) >> 8;
}

