/* Ghidra analysis output; verify against original SH instructions. */

/* Executed810 cases+18 default checks: feedback threshold selects timed decrement
   counters;566Eexact1 enables protected5520 override. Stock step~.05,floor5;entry differs.
   control-policy.txt. */

void Control_UpdateFeedbackOverride(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  char cVar6;
  undefined2 uVar5;
  float fVar7;
  float fVar8;
  float fVar9;
  float fVar10;
  
  fVar7 = (float)(*(code *)PTR_FUN_00021e38)
                           (*(undefined4 *)PTR_ThrottleCandidate_DefaultClosedOffset_00021e30,
                            PTR_DAT_00021e34);
  fVar8 = (float)(*(code *)PTR_FUN_00021e40)(PTR_SCI1_ProtectedFeedbackValue_00021e3c);
  cVar6 = (*(code *)PTR_FUN_00021e48)(PTR_Control_FeedbackOverrideEnabled_00021e44);
  puVar2 = PTR_Control_FeedbackThresholdState_00021e54;
  puVar1 = PTR_DAT_00021e50;
  fVar9 = *(float *)PTR_DAT_00021e4c + fVar7;
  if (fVar8 < fVar9) {
    if (fVar8 < fVar9 - *(float *)PTR_DAT_00021e50) {
      *PTR_Control_FeedbackThresholdState_00021e54 = 0;
    }
  }
  else {
    *PTR_Control_FeedbackThresholdState_00021e54 = 1;
  }
  puVar4 = PTR_Control_AboveThresholdCounter_00021e5c;
  puVar3 = PTR_Control_BelowThresholdCounter_00021e58;
  if (cVar6 == '\x01') {
    if (*PTR_Control_PreviousOverrideEnable_00021e60 == '\0') {
      fVar10 = *(float *)PTR_DAT_00021e64 + fVar7;
      if (fVar8 < fVar10) {
        fVar10 = (float)(*(code *)PTR_FUN_00021e6c)
                                  (fVar9 - *(float *)puVar1,
                                   *(float *)PTR_ThrottleCandidate_RelativeAngle_00021e68 + fVar7);
      }
    }
    else {
      fVar7 = (float)(*(code *)PTR_FUN_00021e40)(PTR_Control_ProtectedFeedbackOverride_00021e28);
      if (*puVar2 == '\x01') {
        if (*(ushort *)PTR_DAT_00021e70 <= *(ushort *)puVar4) {
          fVar7 = fVar7 - *(float *)PTR_DAT_00021e74;
          *(undefined2 *)puVar4 = 0;
        }
        uVar5 = (*(code *)PTR_FUN_00021e78)((int)*(short *)puVar4,1);
        *(undefined2 *)puVar4 = uVar5;
        *(undefined2 *)puVar3 = 0;
      }
      else {
        if (*(ushort *)PTR_DAT_00021e7c <= *(ushort *)puVar3) {
          fVar7 = fVar7 - *(float *)PTR_DAT_00021e80;
          *(undefined2 *)puVar3 = 0;
        }
        uVar5 = (*(code *)PTR_FUN_00021e78)((int)*(short *)puVar3,1);
        *(undefined2 *)puVar3 = uVar5;
        *(undefined2 *)puVar4 = 0;
      }
      fVar10 = (float)(*(code *)PTR_FUN_00021e88)(*(undefined4 *)PTR_DAT_00021e84,fVar7);
    }
  }
  else {
    fVar10 = 0.0;
    *(undefined2 *)PTR_Control_AboveThresholdCounter_00021e5c = 0;
    *(undefined2 *)puVar3 = 0;
  }
  (*(code *)PTR_FUN_00021e2c)(fVar10,PTR_Control_ProtectedFeedbackOverride_00021e28);
  *PTR_Control_PreviousOverrideEnable_00021e60 = cVar6;
  return;
}

