/* Ghidra analysis output; verify against original SH instructions. */

/* 80A4 fromA35EC if80A8>0 and7010zero; elseA35F8 if7EEEnonzero; elseA3610 if75DCexact1; elseA3604.
   Full lookup bodies and knots tested. */

void Control_SelectBaselineSourceDecay(void)

{
  undefined *puVar1;
  undefined *puVar2;
  char cVar3;
  undefined *puVar4;
  undefined4 uVar5;
  
  puVar4 = PTR_FUN_00058ecc;
  puVar2 = PTR_Control_BaselineSourceDecayStep_00058ec8;
  puVar1 = PTR_Lookup_FloatCurve_00058ec4;
  if ((*PTR_Control_BaselineSourceCountdown_00058ed0 == '\0') ||
     (cVar3 = (*(code *)PTR_FUN_00058ed8)(PTR_DAT_00058ed4), cVar3 != '\0')) {
    cVar3 = (*(code *)PTR_FUN_00058ed8)(PTR_DAT_00058ee4);
    if (cVar3 == '\0') {
      cVar3 = (*(code *)PTR_FUN_00058ed8)(PTR_DAT_00058ee8);
      if (cVar3 == '\x01') {
        uVar5 = (*(code *)puVar4)(PTR_DAT_00058edc);
        puVar4 = PTR_Control_BaselineDecaySpecialDescriptor_00058eec;
      }
      else {
        uVar5 = (*(code *)puVar4)(PTR_DAT_00058edc);
        puVar4 = PTR_Control_BaselineDecayDefaultDescriptor_00058ef0;
      }
      uVar5 = (*(code *)puVar1)(uVar5,puVar4);
      *(undefined4 *)puVar2 = uVar5;
    }
    else {
      uVar5 = (*(code *)puVar4)(PTR_DAT_00058edc);
      uVar5 = (*(code *)puVar1)(uVar5,PTR_Control_BaselineDecayExtraDescriptor_00058ef4);
      *(undefined4 *)puVar2 = uVar5;
    }
  }
  else {
    uVar5 = (*(code *)puVar4)(PTR_DAT_00058edc);
    uVar5 = (*(code *)puVar1)(uVar5,PTR_Control_BaselineDecayCountdownDescriptor_00058ee0);
    *(undefined4 *)puVar2 = uVar5;
  }
  return;
}

