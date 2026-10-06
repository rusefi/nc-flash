/* Ghidra analysis output; verify against original SH instructions. */

/* STATIC: long application sequence includes31524(event4,0) at1E6A0; full task unexecuted. No
   proved ratio to timer wheel. */

void Task_ApplicationPeriodicBody(char param_1)

{
  undefined *puVar1;
  int iVar2;
  
  puVar1 = PTR_FUN_0001e6f0;
  *(char *)(int)DAT_0001e6ee = *(char *)(int)DAT_0001e6ee + '\x01';
  (*(code *)puVar1)();
  (*(code *)PTR_Input_UpdateFilteredStates_0001e6f4)();
  (*(code *)PTR_FUN_0001e6f8)();
  (*(code *)PTR_Input_PublishApplicationStates_0001e6fc)();
  (*(code *)PTR_FUN_0001e700)();
  (*(code *)PTR_FUN_0001e704)();
  (*(code *)PTR_FUN_0001e708)();
  (*(code *)PTR_SourceInput_PublishFilteredChannel25_0001e70c)();
  (*(code *)PTR_FUN_0001e710)();
  (*(code *)PTR_CAN215_SelectBaseInput_0001e714)();
  (*(code *)PTR_CAN215_SelectSecondApplicationValue_0001e718)();
  (*(code *)PTR_SparkRequest_ConvertBaseInputs_0001e71c)();
  (*(code *)PTR_FUN_0001e720)();
  (*(code *)PTR_Measurement_UpdateAndSubstitute_0001e724)();
  (*(code *)PTR_FUN_0001e728)();
  (*(code *)PTR_FUN_0001e72c)();
  (*(code *)PTR_ErrorCapture_UpdateTwoSampleMean_0001e730)();
  (*(code *)PTR_FUN_0001e734)();
  (*(code *)PTR_FUN_0001e738)();
  (*(code *)PTR_FUN_0001e73c)();
  (*(code *)PTR_FUN_0001e740)();
  (*(code *)PTR_FUN_0001e744)();
  (*(code *)PTR_FUN_0001e748)();
  (*(code *)PTR_FUN_0001e74c)();
  (*(code *)PTR_FUN_0001e750)();
  (*(code *)PTR_FUN_0001e754)();
  (*(code *)PTR_Phase_DispatchEvent_0001e758)(4,0);
  (*(code *)PTR_thunk_FUN_00030318_0001e75c)();
  (*(code *)PTR_FUN_0001e760)();
  (*(code *)PTR_FUN_0001e764)();
  iVar2 = param_1 * 4;
  (**(code **)(PTR_PTR_0001e768 + iVar2))();
  (**(code **)(PTR_PTR_0001e76c + iVar2))();
  (**(code **)(PTR_PTR_0001e770 + iVar2))();
  (*(code *)PTR_FUN_0001e774)();
  (*(code *)PTR_FUN_0001e778)();
  (*(code *)PTR_FUN_0001e77c)();
  return;
}

