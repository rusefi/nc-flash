/* Ghidra analysis output; verify against original SH instructions. */

/* Fullcaller executed640 times ininput25->source/mode->two-record manager traces. Producesproposal1
   fromfixture2,then48C08 accepts/createscode0. Allsource495C0 outputs independentlychecked;
   Newproducedfault trace:4508A changes1->4 at150,4->1 at211; downstreampair stages preserve it.32
   savedRAM replays isolate809C substitution. Physicalgear unresolved; tcu-fault-selection.txt. */

void Selection_UpdateApplicationIndex(void)

{
  undefined *puVar1;
  undefined *puVar2;
  byte bVar3;
  byte bVar4;
  byte local_14 [4];
  undefined1 auStack_10 [8];
  
  bVar3 = Selection_ApplicationIndex;
  puVar1 = PTR_DAT_00044df0;
  local_14[0] = Selection_ApplicationIndex;
  auStack_10[0] = *PTR_DAT_00044de0;
  if ((*PTR_DAT_00044df4 & 1) == 0) {
    *PTR_DAT_00044df0 = 0;
  }
  puVar2 = PTR_DAT_00044de8;
  if ((byte)*puVar1 < (byte)*PTR_DAT_00044df8) {
    bVar4 = *PTR_DAT_00044de8 | 0x80;
  }
  else {
    bVar4 = *PTR_DAT_00044de8 & 0x7f;
  }
  *PTR_DAT_00044de8 = bVar4;
  *PTR_Selection_PreviousIndex_00044ddc = bVar3;
  Selection_PublishProposalAxis();
  FUN_00045016();
  (*(code *)PTR_StoredAdjustment_RunLifecycle_00044dfc)();
  (*(code *)PTR_Selection_ProduceProposalThresholds_00044e00)();
  Selection_ScanProposalThresholds(local_14,auStack_10);
  (*(code *)PTR_FUN_00044e04)(local_14);
  (*(code *)PTR_SourcePolicy_AdjustProposal_00044e08)(local_14,auStack_10);
  (*(code *)PTR_Selection_RunThreeStagePipeline_00044e0c)(local_14,auStack_10);
  if (((int)(char)*puVar2 & 0x80U) != 0) {
    local_14[0] = (*(code *)PTR_StateCache_ReadByte_00044dd8)(0x12);
  }
  if (TransmissionStateClass == 0xff) {
    local_14[0] = 0;
    auStack_10[0] = 0;
    *PTR_Selection_SourceCode_00044de4 = 0;
  }
  FUN_00045160(local_14,auStack_10);
  puVar1 = PTR_Selection_PreviousIndex_00044ddc;
  if (5 < local_14[0]) {
    local_14[0] = 5;
  }
  Selection_ApplicationIndex = local_14[0];
  *PTR_DAT_00044de0 = auStack_10[0];
  (*(code *)PTR_FUN_00044e10)((int)(char)local_14[0],(int)(char)*puVar1);
  (*(code *)PTR_StateCache_WriteByte_00044dec)(0x12,(int)(char)local_14[0]);
  return;
}

