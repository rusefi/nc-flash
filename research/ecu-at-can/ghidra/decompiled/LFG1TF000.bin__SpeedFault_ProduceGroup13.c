/* Ghidra analysis output; verify against original SH instructions. */

/* Executed gates/counters ->group13 code0722:8900>12 raw3;>6000 raw7. Recovery81
   via58C42/AC89/80B8. See speed-fault.txt for scope. */

void SpeedFault_ProduceGroup13(void)

{
  undefined *puVar1;
  undefined *puVar2;
  char cVar3;
  char cVar4;
  uint uVar5;
  undefined4 uVar6;
  char *pcVar7;
  uint uVar8;
  uint uVar9;
  
  puVar2 = PTR_SpeedFault_Capture0ACount_00058ba0;
  puVar1 = PTR_SpeedFault_OtherCaptureCount_00058b9c;
  uVar8 = 0;
  pcVar7 = (char *)(int)DAT_00058b94;
  uVar6 = 0;
  if ((*PTR_DAT_00058ba4 == '\x01') && (*PTR_DAT_00058ba8 == '\0')) {
    uVar6 = 1;
    if ((int)DAT_00058b96 <= (int)(uint)*(ushort *)PTR_SpeedFault_Capture0ACount_00058ba0) {
      uVar6 = 3;
    }
    if ((*PTR_SpeedFault_Group13Summary_00058bac & 1) != 1) {
      cVar3 = SpeedFault_CheckRecovery();
      if (cVar3 == '\x01') {
        *pcVar7 = '\x01';
      }
      if ((*pcVar7 == '\x01') && (DAT_ffff80b8 == 0)) {
        uVar8 = (uint)DAT_00058b98;
        *PTR_DAT_00058bb0 = 0;
      }
    }
    cVar3 = SpeedFault_CheckSingletonInput();
    cVar4 = SpeedFault_CheckDiagnosticPrerequisites();
    if ((((((*(short *)PTR_DAT_00058bb4 != 0) || ((*PTR_DAT_00058bb8 & 1) != 1)) ||
          ((*PTR_CAN215_InvalidMappedSummary_00058bbc & 1) != 1)) ||
         ((cVar4 != '\x01' || (cVar3 != '\x01')))) ||
        (((int)(uint)*(ushort *)PTR_DAT_00058bc0 < (int)DAT_00058b9a ||
         (((*PTR_DAT_00058bc4 & 1) != 1 || (*PTR_DAT_00058bc8 != '\0')))))) ||
       ((*PTR_DAT_00058bcc != '\0' || ((*PTR_DAT_00058bd0 != '\0' || (*PTR_DAT_00058bd4 != '\0')))))
       ) {
      *(undefined2 *)puVar1 = 0;
      uVar9 = uVar8;
      goto LAB_00058c20;
    }
    uVar9 = uVar8 | 1;
    uVar5 = (uint)*(ushort *)puVar1;
    if (uVar5 <= (uint)*(ushort *)(PTR_DAT_00058c6c + 4) * 0xc) {
      if (0xc < uVar5) {
        *(undefined2 *)puVar2 = 0;
        puVar1 = PTR_DAT_00058c70;
        *pcVar7 = '\0';
        uVar9 = uVar8 & 0x7f | 3;
        *puVar1 = 1;
      }
      goto LAB_00058c20;
    }
    uVar8 = uVar8 & 0x7f | 7;
  }
  else {
    *(undefined2 *)PTR_SpeedFault_OtherCaptureCount_00058b9c = 0;
  }
  *(undefined2 *)puVar2 = 0;
  *pcVar7 = '\0';
  uVar9 = uVar8;
LAB_00058c20:
  (*(code *)PTR_Diagnostic_StoreGroupStatus_00058c74)(0x13,uVar9);
  (*(code *)PTR_Diagnostic_StoreMappedStatus_00058c78)(10,uVar6);
  return;
}

