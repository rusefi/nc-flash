/* Ghidra analysis output; verify against original SH instructions. */

/* StockBB20C0 prioritizes exact1 flags566C/566E/5670/5672;relative orabsolute candidates
   then0..2124 clamp toprotected56A0.324 cases;throttle-candidate.txt. */

void ThrottleCandidate_SelectCommand(void)

{
  undefined *puVar1;
  undefined *puVar2;
  char cVar3;
  undefined *puVar4;
  float fVar5;
  float fVar6;
  undefined4 uVar7;
  
  fVar5 = (float)(*(code *)PTR_FUN_00025798)
                           (*(undefined4 *)PTR_ThrottleCandidate_DefaultClosedOffset_00025790,
                            PTR_DAT_00025794);
  puVar2 = PTR_FUN_000257a4;
  puVar1 = PTR_FUN_00025740;
  puVar4 = PTR_DAT_000257a0;
  if (*PTR_DAT_0002579c != '\x01') {
    cVar3 = (*(code *)PTR_FUN_000257a4)(PTR_DAT_000257a8);
    puVar4 = PTR_Control_HighestOverrideValue_000257ac;
    if (cVar3 == '\x01') {
LAB_000256e4:
      fVar6 = (float)(*(code *)puVar1)(puVar4);
      fVar6 = fVar6 + fVar5;
      goto LAB_0002570c;
    }
    cVar3 = (*(code *)puVar2)(PTR_Control_FeedbackOverrideEnabled_000257b0);
    puVar4 = PTR_Control_ProtectedFeedbackOverride_000257b4;
    if (cVar3 != '\x01') {
      cVar3 = (*(code *)puVar2)(PTR_DAT_000257b8);
      puVar4 = PTR_Control_RelativeOverrideValue_000257bc;
      if (cVar3 == '\x01') goto LAB_000256e4;
      cVar3 = (*(code *)puVar2)(PTR_DAT_000257c0);
      puVar4 = PTR_Control_AbsoluteOverrideValue_000257c4;
      if (cVar3 != '\x01') {
        fVar6 = *(float *)PTR_ThrottleCandidate_RelativeAngle_00025754 + fVar5;
        goto LAB_0002570c;
      }
    }
  }
  fVar6 = (float)(*(code *)puVar1)(puVar4);
LAB_0002570c:
  uVar7 = (*(code *)PTR_FUN_00025798)(*(undefined4 *)PTR_DAT_000257c8,PTR_DAT_000257cc);
  uVar7 = (*(code *)PTR_FUN_00025758)(fVar6,0,uVar7);
  (*(code *)PTR_FUN_00025738)(uVar7,PTR_ThrottleCandidate_SelectedAngle_00025734);
  return;
}

