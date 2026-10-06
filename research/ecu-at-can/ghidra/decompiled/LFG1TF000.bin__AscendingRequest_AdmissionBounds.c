/* Ghidra analysis output; verify against original SH instructions. */

/* Code0..4/default0: first=curve7677E+9*bank(record+14)>>2 (stock256/256/320/320/320);
   second=s16(-80F0)*(curve767AB+9*bank(208F0(80EA))>>8).1470 cases; both outputs signed32 in
   predicates. */

void AscendingRequest_AdmissionBounds(uint *param_1,int *param_2,int param_3)

{
  char cVar1;
  ushort extraout_var;
  undefined4 uVar2;
  uint uVar3;
  undefined *puVar4;
  undefined *puVar5;
  
  cVar1 = *(char *)(param_3 + 1);
  puVar4 = PTR_AscendingRequest_AdmissionDerivativeCurves_36__0004e50c;
  puVar5 = PTR_AscendingRequest_AdmissionOffsetCurves_36__0004e510;
  if ((((cVar1 != '\x04') &&
       (puVar4 = PTR_AscendingRequest_AdmissionDerivativeCurves_27__0004e514,
       puVar5 = PTR_AscendingRequest_AdmissionOffsetCurves_27__0004e518, cVar1 != '\x03')) &&
      (puVar4 = PTR_AscendingRequest_AdmissionDerivativeCurves_18__0004e51c,
      puVar5 = PTR_AscendingRequest_AdmissionOffsetCurves_18__0004e520, cVar1 != '\x02')) &&
     (puVar4 = PTR_AscendingRequest_AdmissionDerivativeCurves_9__0004e524,
     puVar5 = PTR_AscendingRequest_AdmissionOffsetCurves_9__0004e528, cVar1 != '\x01')) {
    puVar4 = PTR_AscendingRequest_AdmissionDerivativeCurves_0004e52c;
    puVar5 = PTR_AscendingRequest_AdmissionOffsetCurves_0004e530;
  }
  uVar2 = (*(code *)PTR_Measurement_ClampAndScaleCurveAxis_0004e534)((int)DAT_ffff80ea);
  (*(code *)PTR_Lookup_ByteCurveToFixedPoint_0004e538)(uVar2,puVar4);
  puVar4 = PTR_Lookup_ByteCurveToFixedPoint_0004e538;
  *param_2 = (int)-Measurement_DerivativeForRequest * (int)(short)(extraout_var & 0xff);
  uVar3 = (*(code *)puVar4)((int)*(short *)(param_3 + 0xe),puVar5);
  *param_1 = (uVar3 & 0xffff) >> 2;
  return;
}

