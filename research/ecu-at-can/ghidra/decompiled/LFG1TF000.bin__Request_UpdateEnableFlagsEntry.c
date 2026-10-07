/* Ghidra analysis output; verify against original SH instructions. */

/* Original126EC phase0/4 enters23BF0, falls through23BF6; updates9410 enable hysteresis, NOT
   request creation.24 selected-byte actual-return checks across96 fulltasks; prior direct gate
   model reused. Actualrequest creation is31524event1. tcu-periodic-request.txt. */

undefined * Request_UpdateEnableFlagsEntry(void)

{
  char cVar1;
  short sVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined *puVar5;
  ushort uVar6;
  ushort uVar7;
  int iVar8;
  uint uVar9;
  uint uVar10;
  undefined *puVar11;
  undefined *puVar12;
  uint uVar13;
  
  sVar2 = DAT_ffff80f6;
  uVar7 = Comparison_ApplicationInput;
  uVar6 = Primary_ApplicationInput;
  puVar5 = PTR_Lookup_ByteCurveToFixedPoint_00023d7c;
  puVar4 = PTR_Request_EnableFallbackCalibration_2__00023d74;
  puVar3 = PTR_Request_EnableFlags_00023d6c;
  if (*PTR_DAT_00023d5c == '\0') {
    iVar8 = (int)Phase_MeasuredSourceSample;
    puVar11 = (undefined *)(uint)Request_CapturedMeasurementScaled;
  }
  else {
    iVar8 = *(int *)(PTR_Phase_ProducedReferenceWords_00023d60 + (uint)Selection_NextIndex * 4);
    puVar11 = (undefined *)
              ((uint)*(ushort *)
                      (PTR_Phase_ReferenceScalesQ12_00023d64 + (uint)Selection_NextIndex * 2) *
               (uint)Request_CapturedSourceAxisRaw >> 0xb);
  }
  puVar12 = (undefined *)(iVar8 << 2);
  if (PTR_DAT_00023d68 < (undefined *)(iVar8 << 2)) {
    puVar12 = PTR_DAT_00023d68;
  }
  if (PTR_DAT_00023d68 < puVar11) {
    puVar11 = PTR_DAT_00023d68;
  }
  if ((*PTR_DAT_00023d70 & 1) == 1) {
    *PTR_Request_EnableFlags_00023d6c = *PTR_Request_EnableFlags_00023d6c | 4;
    cVar1 = *puVar3;
    *puVar3 = (char)(undefined *)((int)cVar1 | 1U);
    if (*(short *)puVar4 <= sVar2) {
LAB_00023d42:
      cVar1 = *puVar3;
      *puVar3 = (char)(undefined *)((int)cVar1 | 2U);
      return (undefined *)((int)cVar1 | 2U);
    }
    if (*(short *)PTR_Request_EnableFallbackCalibration_1__00023d78 <= sVar2) {
      return (undefined *)((int)cVar1 | 1U);
    }
  }
  else {
    uVar9 = (*(code *)PTR_Lookup_ByteCurveToFixedPoint_00023d7c)
                      (puVar12,PTR_Request_EnableCurves_00023d80,0);
    uVar9 = (uVar9 & 0xffff) >> 1;
    uVar13 = (uint)uVar7;
    if (uVar13 < uVar9) {
      *puVar3 = *puVar3 & 0xfb;
    }
    else if (((int)*(short *)PTR_Request_EnableFallbackCalibration_00023d84 + uVar9 & 0xffff) <=
             uVar13) {
      *puVar3 = *puVar3 | 4;
    }
    uVar9 = (*(code *)puVar5)(puVar11,PTR_Request_EnableCurves_00023d80);
    uVar10 = (uVar9 & 0xffff) >> 1;
    sVar2 = *(short *)PTR_Request_EnableFallbackCalibration_00023d84;
    uVar9 = (*(code *)puVar5)(puVar11,PTR_Request_EnableCurves_11__00023d88);
    if ((uVar13 < (uVar9 & 0xffff) >> 1) && (uVar6 < uVar10)) {
      *puVar3 = *puVar3 & 0xfe;
    }
    else if ((ushort)(sVar2 + (short)uVar10) <= uVar6) {
      *puVar3 = *puVar3 | 1;
    }
    uVar9 = (uint)(char)CAN231_SixStateSource;
    if (4 < CAN231_SixStateSource) {
      uVar9 = 4;
    }
    uVar10 = (*(code *)puVar5)((int)Request_CapturedSourceAxisScaled,
                               PTR_Request_EnableCurves_22__00023d8c + (uVar9 & 0xff) * 0xb);
    uVar10 = (uVar10 & 0xffff) >> 1;
    if (uVar10 <= uVar13) {
      if (uVar13 < ((int)*(short *)(PTR_Request_EnableUpperGaps_00023d90 + (uVar9 & 0xff) * 2) +
                    uVar10 & 0xffff)) {
        return PTR_Request_EnableUpperGaps_00023d90;
      }
      goto LAB_00023d42;
    }
  }
  cVar1 = *puVar3;
  *puVar3 = (char)(undefined *)((int)cVar1 & 0xfdU);
  return (undefined *)((int)cVar1 & 0xfdU);
}

