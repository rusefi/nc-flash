/* Ghidra analysis output; verify against original SH instructions. */

/* Code0..4/default0: word76742+12*code+2*u8(record+12), stock51 for six slots.
   Dynamic=s16(-s16(80F0))*(curve767D8+9*code(208F0(80EA))>>8).2016 cases. */

void AscendingRequest_ReleaseBounds(undefined2 *param_1,int *param_2,int param_3)

{
  char cVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined *puVar5;
  ushort extraout_var;
  undefined4 uVar6;
  int iVar7;
  undefined *puVar8;
  
  puVar5 = PTR_AscendingRequest_ReleaseDerivativeCurves_0004e590;
  puVar4 = PTR_AscendingRequest_ReleaseDerivativeCurves_9__0004e588;
  puVar3 = PTR_AscendingRequest_ReleaseDerivativeCurves_18__0004e580;
  puVar2 = PTR_AscendingRequest_ReleaseDerivativeCurves_27__0004e578;
  puVar8 = PTR_AscendingRequest_ReleaseDerivativeCurves_36__0004e570;
  cVar1 = *(char *)(param_3 + 1);
  iVar7 = (uint)*(byte *)(param_3 + 0xc) * 2;
  if (cVar1 == '\x04') {
    *param_1 = *(undefined2 *)(PTR_AscendingRequest_ReleaseMinimums_24__0004e574 + iVar7);
  }
  else if (cVar1 == '\x03') {
    *param_1 = *(undefined2 *)(PTR_AscendingRequest_ReleaseMinimums_18__0004e57c + iVar7);
    puVar8 = puVar2;
  }
  else if (cVar1 == '\x02') {
    *param_1 = *(undefined2 *)(PTR_AscendingRequest_ReleaseMinimums_12__0004e584 + iVar7);
    puVar8 = puVar3;
  }
  else if (cVar1 == '\x01') {
    *param_1 = *(undefined2 *)(PTR_AscendingRequest_ReleaseMinimums_6__0004e58c + iVar7);
    puVar8 = puVar4;
  }
  else {
    *param_1 = *(undefined2 *)(PTR_AscendingRequest_ReleaseMinimums_0004e594 + iVar7);
    puVar8 = puVar5;
  }
  uVar6 = (*(code *)PTR_Measurement_ClampAndScaleCurveAxis_0004e534)((int)DAT_ffff80ea);
  (*(code *)PTR_Lookup_ByteCurveToFixedPoint_0004e538)(uVar6,puVar8);
  *param_2 = (int)-Measurement_DerivativeForRequest * (int)(short)(extraout_var & 0xff);
  return;
}

