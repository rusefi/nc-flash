/* Ghidra analysis output; verify against original SH instructions. */

/* StockBAEA0=1: clamp((72FC+6D00)*BACA8,0,BAEA4) to569C.54 cases. Savedromdrop labels
   multiplier/max as throttleangle;physical actuator notverified. */

void ThrottleCandidate_ConvertSelectedValue(void)

{
  undefined *puVar1;
  float fVar2;
  float fVar3;
  undefined4 uVar4;
  
  fVar2 = (float)(*(code *)PTR_FUN_00025740)(PTR_Control_BoundedOverrideSource_0002573c);
  fVar2 = *(float *)PTR_DAT_00025744 + fVar2;
  fVar3 = (float)(*(code *)PTR_FUN_00025750)
                           (0x3f800000,DAT_00025748,(int)*(short *)PTR_DAT_0002574c);
  puVar1 = PTR_ThrottleCandidate_RelativeAngle_00025754;
  uVar4 = *(undefined4 *)PTR_ThrottleCandidate_MaximumAngle_0002575c;
  if (*PTR_DAT_00025760 == '\0') {
    if (((*PTR_DAT_00025770 != '\0') || (*PTR_DAT_00025774 != '\x01')) ||
       (*(float *)PTR_Model_NetCountScaledValue_00025778 <= fVar3)) {
      if (*PTR_DAT_00025780 != '\x01') {
        if (*PTR_DAT_00025788 == '\x01') {
          uVar4 = *(undefined4 *)PTR_DAT_0002578c;
        }
        uVar4 = (*(code *)PTR_FUN_00025758)(fVar2,0,uVar4);
        *(undefined4 *)puVar1 = uVar4;
        return;
      }
      uVar4 = *(undefined4 *)PTR_DAT_00025784;
    }
    else {
      uVar4 = *(undefined4 *)PTR_DAT_0002577c;
    }
  }
  else {
    fVar2 = (*(float *)PTR_Control_NormalCommandOffset_00025768 +
            *(float *)PTR_Control_SelectedPublishedValue_00025764) *
            *(float *)PTR_ThrottleCandidate_AngleMultiplier_0002576c;
  }
  uVar4 = (*(code *)PTR_FUN_00025758)(fVar2,0,uVar4);
  *(undefined4 *)puVar1 = uVar4;
  return;
}

