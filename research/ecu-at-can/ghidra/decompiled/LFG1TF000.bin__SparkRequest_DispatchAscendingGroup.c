/* Ghidra analysis output; verify against original SH instructions. */

/* Group7 dispatcher via2FEF8 descriptorB08C. Code1 creation,map,release andreactivation now
   executed throughCAN216/ECU. Natural8081=2 reselects live map on rebound; forced0 stays in
   captured release. See tcu-ascending-map/release/predicates.txt; complete phase qualification
   remains open. */

void SparkRequest_DispatchAscendingGroup(undefined4 param_1,undefined4 param_2)

{
  (*(code *)PTR_CallbackState_Dispatch_0004def0)(param_1,param_2,DAT_0004deec);
  return;
}

