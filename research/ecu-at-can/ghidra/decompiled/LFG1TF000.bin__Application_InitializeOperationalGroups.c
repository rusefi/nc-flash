/* Ghidra analysis output; verify against original SH instructions. */

/* Three fulloriginalcalls PASS; native62-callsegment1E08E..1E254 wholeRAM matches62explicitcalls
   fromsamestate. Fullnative vslegacyfixture differs209RAMbytes: preceding/followinginitializers
   matter. Differentialnotindependentsemanticoracle. tcu-native-group-initialization.txt. */

void Application_InitializeOperationalGroups(void)

{
  (*(code *)PTR_EventQueue_Initialize_0001e25c)(0);
  (*(code *)PTR_Heap_InitializeRequestStorage_0001e260)();
  (*(code *)PTR_EventMessage_InitializeBufferIndex_0001e264)();
  FUN_0001e3d0();
  FUN_0001ed94();
  FUN_0001e40e();
  (*(code *)PTR_FUN_0001e268)();
  (*(code *)PTR_FUN_0001e26c)();
  (*(code *)PTR_FUN_0001e270)();
  (*(code *)PTR_FUN_0001e274)();
  (*(code *)PTR_FUN_0001e278)();
  (*(code *)PTR_FUN_0001e27c)();
  (*(code *)PTR_FUN_0001e280)();
  (*(code *)PTR_FUN_0001e284)();
  (*(code *)PTR_FUN_0001e288)();
  (*(code *)PTR_FUN_0001e28c)();
  (*(code *)PTR_FUN_0001e290)();
  (*(code *)PTR_DiscreteOutput_InitSlots_0001e294)();
  (*(code *)PTR_FUN_0001e298)();
  (*(code *)PTR_SparkRequest_InitializeRecords_0001e29c)();
  (*(code *)PTR_FUN_0001e2a0)();
  FUN_0001ed8c();
  (*(code *)PTR_FUN_0001e2a4)();
  (*(code *)PTR_FUN_0001e2a8)();
  (*(code *)PTR_FUN_0001e2ac)();
  (*(code *)PTR_thunk_FUN_00030160_0001e2b0)();
  (*(code *)PTR_FUN_0001e2b4)();
  (*(code *)PTR_ErrorCapture_Initialize_0001e2b8)();
  (*(code *)PTR_AdjustmentTimers_InitializeCallbackState_0001e2bc)();
  (*(code *)PTR_Phase_DispatchEvent_0001e2c0)(0);
  (*(code *)PTR_FUN_0001e2c4)(0);
  (*(code *)PTR_FUN_0001e2c8)();
  (*(code *)PTR_FUN_0001e2cc)(0);
  (*(code *)PTR_FUN_0001e2d0)(0);
  (*(code *)PTR_FUN_0001e2d4)(0);
  (*(code *)PTR_FUN_0001e2d8)();
  (*(code *)PTR_FUN_0001e2dc)(0);
  (*(code *)PTR_FUN_0001e2e0)(0);
  (*(code *)PTR_ClassApplication_InitPriorityList_0001e2e4)();
  (*(code *)PTR_FUN_0001e2e8)();
  (*(code *)PTR_ClassAdjustment_LoadUniformCount_0001e2ec)();
  (*(code *)PTR_FUN_0001e2f0)(0);
  (*(code *)PTR_FUN_0001e2f4)(0);
  (*(code *)PTR_FUN_0001e2f8)(0);
  (*(code *)PTR_FUN_0001e2fc)(0);
  (*(code *)PTR_FUN_0001e300)(0);
  (*(code *)PTR_FUN_0001e304)(0);
  (*(code *)PTR_FUN_0001e308)(0);
  (*(code *)PTR_FUN_0001e30c)(0);
  (*(code *)PTR_FUN_0001e310)(0);
  (*(code *)PTR_FUN_0001e314)();
  (*(code *)PTR_FUN_0001e318)();
  (*(code *)PTR_FUN_0001e31c)();
  (*(code *)PTR_SourcePolicy_InitializeState_0001e320)();
  (*(code *)PTR_FUN_0001e324)();
  (*(code *)PTR_Selection_InitializeAcceptedState_0001e328)();
  (*(code *)PTR_TransitionProgress_InitializeFromAccepted_0001e32c)();
  (*(code *)PTR_FUN_0001e330)(0);
  (*(code *)PTR_FUN_0001e334)(0);
  (*(code *)PTR_SparkRequest_InitializeFirstList_0001e338)();
  (*(code *)PTR_SparkRequest_DispatchManager_0001e33c)(0);
  (*(code *)PTR_SparkRequest_InitializeSecondList_0001e340)();
  (*(code *)PTR_FUN_0001e344)(0);
  (*(code *)PTR_SparkRequest_DispatchFirstListState_0001e348)(0);
  (*(code *)PTR_SparkRequest_DispatchAscendingGroup_0001e34c)(0);
  (*(code *)PTR_FUN_0001e350)(0);
  (*(code *)PTR_FUN_0001e354)(0);
  (*(code *)PTR_FUN_0001e358)(0);
  (*(code *)PTR_FUN_0001e35c)();
  (*(code *)PTR_FUN_0001e360)();
  (*(code *)PTR_FUN_0001e364)(0);
  (*(code *)PTR_FUN_0001e368)(0);
  (*(code *)PTR_FUN_0001e36c)(0);
  (*(code *)PTR_FUN_0001e370)(0);
  (*(code *)PTR_FUN_0001e374)();
  (*(code *)PTR_FUN_0001e378)(0);
  (*(code *)PTR_FUN_0001e37c)(0);
  (*(code *)PTR_FUN_0001e380)(0);
  (*(code *)PTR_FUN_0001e384)(0);
  (*(code *)PTR_FUN_0001e388)(0);
  (*(code *)PTR_FUN_0001e38c)(0);
  (*(code *)PTR_FUN_0001e390)();
  (*(code *)PTR_FUN_0001e394)(0);
  (*(code *)PTR_FUN_0001e398)(0);
  (*(code *)PTR_FUN_0001e39c)(0);
  (*(code *)PTR_FUN_0001e3a0)(0);
  (*(code *)PTR_FUN_0001e3a4)(0);
  (*(code *)PTR_FUN_0001e3a8)(0);
  (*(code *)PTR_FUN_0001e50c)(0);
  (*(code *)PTR_FUN_0001e510)(0);
  (*(code *)PTR_FUN_0001e514)();
  (*(code *)PTR_FUN_0001e518)();
  (*(code *)PTR_thunk_FUN_0002c064_0001e51c)();
  return;
}

