/* Ghidra analysis output; verify against original SH instructions. */

/* States0..4 retry HCAN reset/halt recovery;8BCE saturates255. Delays40 ticks below10 retries,1000
   thereafter.47-checkpoint lifecycle and240 boundary cases; explicit register samples. */

uint HCAN_ProcessRecoveryState(byte param_1)

{
  ushort uVar1;
  undefined *puVar2;
  uint uVar3;
  uint uVar4;
  char cVar6;
  short sVar5;
  undefined4 *puVar7;
  byte bVar9;
  undefined1 *puVar8;
  char *pcVar10;
  byte *pbVar11;
  char *pcVar12;
  uint *puVar13;
  
  uVar3 = (*(code *)PTR_Tick_Read_0001a22c)();
  pcVar10 = (char *)(int)DAT_0001a210;
  puVar13 = (uint *)(int)DAT_0001a216;
  pbVar11 = (byte *)(int)DAT_0001a212;
  pcVar12 = (char *)(int)DAT_0001a214;
  uVar4 = (uint)param_1;
  if (uVar4 == 0) {
    *(undefined1 *)(int)DAT_0001a218 = 1;
    *(undefined1 *)(int)DAT_0001a21a = 0;
    *pbVar11 = 0;
    *pcVar12 = '\x02';
    *puVar13 = 0;
    puVar7 = (undefined4 *)(int)DAT_0001a21e;
    *(undefined1 *)(int)DAT_0001a21c = 2;
    *puVar7 = 0;
    *pcVar10 = '\0';
    HCAN_ProduceDiagnosticGroup35(0);
    uVar3 = FUN_0001a966(0);
    *(undefined1 *)(int)DAT_0001a220 = 0;
    return uVar3;
  }
  if (uVar4 != 1) {
    if (uVar4 != 7) {
      return uVar4;
    }
    *(undefined1 *)(int)DAT_0001a42a = 1;
    *(undefined1 *)(int)DAT_0001a42e = 0;
    *pbVar11 = 0;
    *pcVar12 = '\x02';
    *puVar13 = 0;
    return 7;
  }
  cVar6 = *pcVar10;
  if (cVar6 == '\0') {
    sVar5 = (*(code *)PTR_HCAN_ReadConfigurationStatus_0001a230)();
    if (sVar5 != 0) goto LAB_0001a3ca;
    if (*pcVar12 == '\x01') goto LAB_0001a25c;
  }
  else {
    if (cVar6 == '\x01') {
      if (*(char *)(int)DAT_0001a306 != '\x01') {
        *(undefined1 *)(int)DAT_0001a30a = 0;
        goto LAB_0001a3ca;
      }
      *(undefined1 *)(int)DAT_0001a308 = 2;
      *(undefined1 *)(int)DAT_0001a30a = 1;
      *pcVar12 = '\x01';
      if (*pbVar11 < 10) {
        uVar3 = uVar3 + 0x28;
      }
      else {
        uVar3 = uVar3 + (int)DAT_0001a30c;
      }
      *puVar13 = uVar3;
LAB_0001a25c:
      *pcVar10 = '\x02';
      goto LAB_0001a3ca;
    }
    if (cVar6 != '\x02') {
      if (cVar6 == '\x03') {
        sVar5 = (*(code *)PTR_HCAN_ReadConfigurationStatus_0001a430)();
        if ((sVar5 == 1) ||
           (bVar9 = *(byte *)(int)DAT_0001a422 + 1, *(byte *)(int)DAT_0001a422 = bVar9, 3 < bVar9))
        {
          (*(code *)PTR_HCAN_SetResetRequest_0001a434)(0);
          *pcVar10 = '\x04';
        }
      }
      else if ((cVar6 == '\x04') &&
              (sVar5 = (*(code *)PTR_HCAN_ReadConfigurationStatus_0001a430)(), sVar5 == 0)) {
        (*(code *)PTR_FUN_0001a438)(1);
        (*(code *)PTR_FUN_0001a43c)(1);
        puVar8 = (undefined1 *)(int)DAT_0001a426;
        *(undefined1 *)(int)DAT_0001a424 = 0;
        *puVar8 = 2;
        puVar2 = PTR_FUN_0001a440;
        *(undefined4 *)(int)DAT_0001a428 = 0;
        (*(code *)puVar2)();
        (*(code *)PTR_FUN_0001a444)();
        (*(code *)PTR_FUN_0001a448)();
        (*(code *)PTR_FUN_0001a44c)();
        (*(code *)PTR_FUN_0001a450)();
        *(undefined1 *)(int)DAT_0001a42a = 1;
        *pcVar12 = '\x01';
        if (*pbVar11 < 10) {
          uVar3 = *puVar13 + 0x28;
        }
        else {
          uVar3 = *puVar13 + (int)DAT_0001a42c;
        }
        *puVar13 = uVar3;
        *pcVar10 = '\0';
      }
      goto LAB_0001a3ca;
    }
    if (*pcVar12 == '\x01') {
      if (uVar3 < *puVar13) goto LAB_0001a3ca;
      sVar5 = (*(code *)PTR_HCAN_ReadHaltRequest_0001a318)();
      cVar6 = (*(code *)PTR_HCAN_ReadErrorWarningStatus_0001a31c)();
      uVar1 = DAT_0001a30e;
      if (((sVar5 == 1) || (*(char *)(int)DAT_0001a306 == '\x01')) || (cVar6 == '\x01')) {
        *(undefined1 *)(int)DAT_0001a30a = 1;
        *pcVar12 = '\x02';
        if (*pbVar11 != uVar1) {
          *pbVar11 = *pbVar11 + 1;
        }
        (*(code *)PTR_HCAN_SetHaltRequest_0001a320)(0);
        (*(code *)PTR_HCAN_SetResetRequest_0001a324)(1);
        *(undefined1 *)(int)DAT_0001a310 = 0;
        *pcVar10 = '\x03';
        goto LAB_0001a3ca;
      }
      *pcVar12 = '\x02';
      *puVar13 = 0;
      *(undefined1 *)(int)DAT_0001a312 = 2;
      *(undefined4 *)(int)DAT_0001a314 = 0;
      *(undefined1 *)(int)DAT_0001a306 = 0;
      puVar2 = PTR_FUN_0001a328;
      *(undefined1 *)(int)DAT_0001a308 = 1;
      (*(code *)puVar2)();
      (*(code *)PTR_FUN_0001a32c)();
      (*(code *)PTR_FUN_0001a330)();
      (*(code *)PTR_FUN_0001a334)();
      (*(code *)PTR_FUN_0001a338)();
      *(undefined1 *)(int)DAT_0001a30a = 0;
      *pbVar11 = 0;
    }
  }
  *pcVar10 = '\x01';
LAB_0001a3ca:
  uVar3 = HCAN_ProduceDiagnosticGroup35(1);
  return uVar3;
}

