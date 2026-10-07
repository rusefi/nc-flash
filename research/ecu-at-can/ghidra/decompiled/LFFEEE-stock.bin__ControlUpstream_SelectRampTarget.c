/* Ghidra analysis output; verify against original SH instructions. */

/* 6081 direct cases across this body and8BB20; eight target branches with retention, protected2160
   fallback, capped or uncapped ramp.54 original caller checks,32 retained calls,320 paired cycles.
   See control-upstream-target.txt; cross-task cadence unproved. */

void ControlUpstream_SelectRampTarget(void)

{
  char cVar1;
  char cVar2;
  char cVar3;
  char cVar4;
  undefined *puVar5;
  undefined *puVar6;
  float *pfVar7;
  undefined4 uVar8;
  undefined4 uVar9;
  float fVar10;
  float fVar11;
  undefined4 uVar12;
  
  fVar11 = *(float *)PTR_ControlUpstream_ProducedTarget_000311ac;
  uVar12 = *(undefined4 *)PTR_TargetInput_Produced_000311b0;
  uVar8 = (*(code *)PTR_FUN_000311bc)(*(undefined4 *)PTR_DAT_000311b4,PTR_DAT_000311b8);
  puVar5 = PTR_Lookup_FloatCurve_000311d0;
  cVar1 = *PTR_DAT_000311c0;
  cVar2 = *PTR_DAT_000311c4;
  cVar3 = *PTR_DAT_000311c8;
  cVar4 = *PTR_DAT_000311cc;
  uVar9 = (*(code *)PTR_Lookup_FloatCurve_000311d0)(uVar12,PTR_PTR_000311d4);
  *(undefined4 *)PTR_DAT_000311d8 = uVar9;
  uVar9 = (*(code *)puVar5)(uVar12,PTR_PTR_000311dc);
  *(undefined4 *)PTR_DAT_000311e0 = uVar9;
  uVar9 = (*(code *)puVar5)(uVar12,PTR_PTR_000311e4);
  *(undefined4 *)PTR_DAT_000311e8 = uVar9;
  uVar9 = (*(code *)puVar5)(uVar12,PTR_PTR_000311ec);
  *(undefined4 *)PTR_DAT_000311f0 = uVar9;
  uVar9 = (*(code *)puVar5)(uVar12,PTR_PTR_000311f4);
  puVar6 = PTR_LAB_00031200;
  *(undefined4 *)PTR_DAT_000311f8 = uVar9;
  puVar5 = PTR_Lookup_FloatMap2D_000311fc;
  uVar9 = (*(code *)PTR_Lookup_FloatMap2D_000311fc)(uVar8,uVar12,puVar6);
  puVar6 = PTR_LAB_00031208;
  *(undefined4 *)PTR_DAT_00031204 = uVar9;
  uVar9 = (*(code *)puVar5)(uVar8,uVar12,puVar6);
  puVar6 = PTR_LAB_00031210;
  *(undefined4 *)PTR_DAT_0003120c = uVar9;
  uVar8 = (*(code *)puVar5)(uVar8,uVar12,puVar6);
  *(undefined4 *)PTR_DAT_00031214 = uVar8;
  puVar5 = PTR_ControlUpstream_SelectedTarget_0003121c;
  fVar10 = *(float *)PTR_DAT_000311d8;
  if (((((int)(char)*PTR_ControlMode_SelectedBit_00031218 & 0x80U) != 0) && (cVar1 == '\0')) &&
     (cVar2 == '\0')) {
    pfVar7 = (float *)PTR_DAT_000311e0;
    if ((cVar3 != '\x01') && (cVar4 != '\x01')) {
      pfVar7 = (float *)PTR_DAT_000311e8;
    }
    *(float *)PTR_ControlUpstream_SelectedTarget_0003121c = fVar10 + *pfVar7;
    goto LAB_0003116c;
  }
  pfVar7 = (float *)PTR_TargetAdjustment_Retained_00031220;
  if (((cVar1 != '\x01') && (cVar2 != '\x01')) && ((*PTR_ControlMode_SelectedBit_00031218 & 8) == 0)
     ) {
    if ((*PTR_ControlMode_SelectedBit_00031218 & 0x10) != 0) {
      pfVar7 = (float *)PTR_DAT_000311f0;
      if ((cVar3 != '\x01') && (cVar4 != '\x01')) {
        pfVar7 = (float *)PTR_DAT_000311f8;
      }
      *(float *)PTR_ControlUpstream_SelectedTarget_0003121c = fVar10 + *pfVar7;
      goto LAB_0003116c;
    }
    pfVar7 = (float *)PTR_DAT_00031204;
    if ((*PTR_ControlMode_SelectedBit_00031218 & 4) == 0) {
      if ((*PTR_ControlMode_SelectedBit_00031218 & 0x20) == 0) {
        if ((*PTR_ControlMode_SelectedBit_00031218 & 0x40) == 0) {
          if ((*PTR_ControlMode_SelectedBit_00031218 & 1) == 1) {
            *(float *)PTR_ControlUpstream_SelectedTarget_0003121c = fVar10;
          }
        }
        else {
          if ((cVar3 == '\0') && (cVar4 == '\0')) {
            fVar10 = fVar10 + *(float *)PTR_DAT_00031214;
          }
          *(float *)PTR_ControlUpstream_SelectedTarget_0003121c = fVar10;
        }
      }
      else {
        if ((cVar3 == '\0') && (cVar4 == '\0')) {
          fVar10 = fVar10 + *(float *)PTR_DAT_0003120c;
        }
        *(float *)PTR_ControlUpstream_SelectedTarget_0003121c = fVar10;
      }
      goto LAB_0003116c;
    }
  }
  *(float *)PTR_ControlUpstream_SelectedTarget_0003121c = fVar10 + *pfVar7;
LAB_0003116c:
  puVar6 = PTR_FUN_00031224;
  fVar10 = (float)(*(code *)PTR_FUN_00031224)(*(undefined4 *)puVar5,*(undefined4 *)PTR_DAT_00031228)
  ;
  *(float *)PTR_ControlUpstream_CappedTarget_0003122c = fVar10;
  if (*PTR_DAT_00031238 == '\x01') {
    if (fVar10 < fVar11) {
      uVar8 = (*(code *)PTR_FUN_00031454)(fVar11 - *(float *)PTR_TargetRamp_FallStep_00031234);
    }
    else {
      uVar8 = (*(code *)puVar6)(*(float *)PTR_TargetRamp_RiseStep_00031230 + fVar11);
    }
  }
  else if (*(float *)puVar5 < fVar11) {
    uVar8 = (*(code *)PTR_FUN_00031454)(fVar11 - *(float *)PTR_TargetRamp_FallStep_00031234);
  }
  else {
    uVar8 = (*(code *)puVar6)(*(float *)PTR_TargetRamp_RiseStep_00031230 + fVar11);
  }
  puVar5 = PTR_ControlUpstream_ApplyDescriptorOverride_0003145c;
  *(undefined4 *)PTR_ControlUpstream_RampCandidate_00031458 = uVar8;
  uVar8 = (*(code *)puVar5)();
  *(undefined4 *)PTR_ControlUpstream_ProducedTarget_00031460 = uVar8;
  return;
}

