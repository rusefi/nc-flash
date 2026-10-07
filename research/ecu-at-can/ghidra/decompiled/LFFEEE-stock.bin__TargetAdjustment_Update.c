/* Ghidra analysis output; verify against original SH instructions. */

/* Always protected2160/A3900->67F8; prioritizedclear/map/retain/increment67F4. Nonzero6940
   integrates0.1*error at inclusive abs>=1, no
   clamp.Conditionalgate3786direct/36caller/40retained/320pairedcycles. Original31E56 stockDB0C0=0
   disablesincrement. See control-target-adjustment.txt. */

uint TargetAdjustment_Update(void)

{
  char cVar1;
  byte bVar2;
  char cVar3;
  char cVar4;
  bool bVar5;
  undefined *puVar6;
  undefined *puVar7;
  uint uVar8;
  undefined *puVar9;
  undefined4 uVar10;
  float extraout_fr0;
  undefined4 extraout_fr0_00;
  undefined4 extraout_fr0_01;
  float fVar11;
  undefined4 uVar12;
  
  puVar9 = PTR_TargetAdjustment_MappedReference_00030f58;
  puVar6 = PTR_Lookup_FloatCurve_00030ef0;
  cVar1 = *PTR_DAT_00030f40;
  bVar2 = *PTR_DAT_00030f44;
  bVar5 = (*PTR_ControlMode_SelectedBit_00030f48 & 8) == 0;
  cVar3 = *PTR_DAT_00030f4c;
  cVar4 = *PTR_DAT_00030f50;
  uVar12 = *(undefined4 *)PTR_TargetInput_Produced_00030edc;
  fVar11 = *(float *)PTR_DAT_00030f54;
  uVar10 = (*(code *)PTR_FUN_00030f64)(*(undefined4 *)PTR_DAT_00030f5c,PTR_DAT_00030f60);
  uVar10 = (*(code *)puVar6)(uVar10,PTR_LAB_00030f68);
  puVar7 = PTR_FUN_00030f6c;
  *(undefined4 *)puVar9 = uVar10;
  uVar8 = (*(code *)puVar7)(uVar10,fVar11);
  puVar7 = PTR_TargetAdjustment_Retained_00030f70;
  if ((((cVar1 == '\0') && (bVar2 == 0)) && (bVar5)) ||
     (uVar8 = (uint)(byte)*PTR_TargetAdjustment_Inhibit_00030f34, uVar8 == 1)) {
    *(undefined4 *)PTR_TargetAdjustment_Retained_00030f70 = 0;
  }
  else if (*PTR_TargetAdjustment_IncrementGate_00030f74 == '\0') {
    if ((cVar1 == '\x01') || (!bVar5)) {
      puVar9 = PTR_PTR_00030f78;
      if ((cVar3 != '\x01') && (cVar4 != '\x01')) {
        puVar9 = PTR_PTR_00030f7c;
      }
      uVar8 = (*(code *)puVar6)(uVar12,puVar9);
      *(undefined4 *)puVar7 = extraout_fr0_00;
    }
    else {
      uVar8 = (uint)bVar2;
      if (uVar8 == 1) {
        if ((cVar3 == '\x01') || (puVar9 = PTR_PTR_00030f84, cVar4 == '\x01')) {
          puVar9 = PTR_PTR_00030f80;
        }
        uVar8 = (*(code *)puVar6)(uVar12,puVar9);
        *(undefined4 *)puVar7 = extraout_fr0_01;
      }
    }
  }
  else if (*(float *)PTR_DAT_000311a4 <= extraout_fr0) {
    *(float *)PTR_TargetAdjustment_Retained_00030f70 =
         *(float *)PTR_TargetAdjustment_Retained_00030f70 +
         (*(float *)puVar9 - fVar11) * *(float *)PTR_DAT_000311a8;
  }
  return uVar8;
}

