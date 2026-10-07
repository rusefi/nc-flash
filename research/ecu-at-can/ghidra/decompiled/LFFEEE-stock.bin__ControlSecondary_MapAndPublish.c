/* Ghidra analysis output; verify against original SH instructions. */

/* 69A0zero unlessabs6808>.48828125,6937!=1,695Bbit1clear; elsemapA38E8/A38F4 clamp/min.8B960 may
   substitute evenafterzeroing;15522->protected684C.3409cases,72six/72twentycallreplays,320cycles.
    */

void ControlSecondary_MapAndPublish(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  char cVar4;
  undefined4 uVar5;
  undefined4 uVar6;
  
  uVar6 = 0;
  cVar4 = (*(code *)PTR_FUN_00031b68)
                    (*(undefined4 *)PTR_Control_BoundedInputTermSum_00031b88,0,DAT_00031b84);
  puVar3 = PTR_ControlSecondary_MappedCandidate_00031b8c;
  if (((cVar4 == '\0') || (*PTR_ControlSecondary_Gate_00031b90 == '\x01')) ||
     ((*PTR_ControlMode_SelectedBit_00031b94 & 2) != 0)) {
    *(undefined4 *)PTR_ControlSecondary_MappedCandidate_00031b8c = uVar6;
  }
  else {
    uVar5 = (*(code *)PTR_Lookup_FloatCurve_00031b9c)
                      (*(undefined4 *)PTR_ControlSecondary_ScaledTarget_00031b80,PTR_PTR_00031b98);
    puVar2 = PTR_FUN_00031b70;
    puVar1 = PTR_DAT_00031b6c;
    *(undefined4 *)PTR_DAT_00031ba0 = uVar5;
    uVar5 = (*(code *)puVar2)(puVar1);
    uVar5 = (*(code *)PTR_Lookup_FloatCurve_00031b9c)(uVar5,PTR_PTR_00031ba4);
    puVar1 = PTR_DAT_00031ba0;
    *(undefined4 *)PTR_DAT_00031ba8 = uVar5;
    uVar6 = (*(code *)PTR_FUN_00031b78)(*(undefined4 *)puVar1,uVar6,DAT_00031bac);
    *(undefined4 *)puVar3 = uVar6;
    uVar6 = (*(code *)PTR_FUN_00031bb0)(uVar6,*(undefined4 *)PTR_DAT_00031ba8);
    *(undefined4 *)puVar3 = uVar6;
  }
  uVar6 = (*(code *)PTR_ControlSecondary_ApplyDescriptorOverride_00031bb4)(*(undefined4 *)puVar3);
  (*(code *)PTR_FUN_00031bbc)(uVar6,PTR_ControlSecondary_ProtectedPublishedValue_00031bb8);
  return;
}

