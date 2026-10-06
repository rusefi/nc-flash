/* Ghidra analysis output; verify against original SH instructions. */

/* Full38byte record5592 selectiveupdate.56A0 quantized identically at+4/+6;flags
   andprotectedlimits.768 cases. Transport/remote actuator unverified. */

void Control_PackOutgoingCommandRecord(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined *puVar5;
  undefined *puVar6;
  char cVar8;
  char cVar9;
  char cVar10;
  undefined2 uVar7;
  byte *pbVar11;
  undefined4 uVar12;
  undefined4 uVar13;
  undefined4 uVar14;
  
  puVar1 = PTR_FUN_0002272c;
  cVar8 = (*(code *)PTR_FUN_0002272c)(PTR_DAT_00022738);
  cVar9 = (*(code *)puVar1)(PTR_DAT_0002273c);
  puVar2 = PTR_DAT_00022740;
  if ((((cVar9 == '\x01') || (*PTR_DAT_00022744 == '\x01')) || (*PTR_DAT_00022748 == '\x01')) ||
     (cVar10 = (*(code *)puVar1)(PTR_DAT_0002274c), cVar10 == '\x01')) {
    *puVar2 = 1;
  }
  else {
    *puVar2 = 0;
  }
  puVar4 = PTR_Control_OutgoingCommandRecord_00022758;
  puVar3 = PTR_FUN_00022754;
  uVar14 = 0;
  uVar13 = DAT_00022750;
  uVar12 = (*(code *)PTR_FUN_00022760)(PTR_ThrottleCandidate_SelectedAngle_0002275c);
  uVar7 = (*(code *)puVar3)(uVar12,uVar13,uVar14);
  puVar5 = PTR_FUN_00022764;
  *(undefined2 *)(puVar4 + 4) = uVar7;
  *(undefined2 *)(puVar4 + 6) = *(undefined2 *)(puVar4 + 4);
  uVar12 = (*(code *)puVar5)(*(undefined4 *)PTR_ThrottleCandidate_DefaultClosedOffset_00022768,
                             PTR_DAT_0002276c);
  uVar7 = (*(code *)puVar3)(uVar12,uVar13,uVar14);
  *(undefined2 *)(puVar4 + 8) = uVar7;
  uVar12 = (*(code *)puVar5)(*(undefined4 *)PTR_ThrottleCandidate_DefaultClosedOffset_00022768,
                             PTR_DAT_00022770);
  uVar7 = (*(code *)puVar3)(uVar12,uVar13,uVar14);
  *(undefined2 *)(puVar4 + 10) = uVar7;
  uVar12 = (*(code *)puVar5)(*(undefined4 *)PTR_DAT_00022774,PTR_DAT_00022778);
  uVar7 = (*(code *)puVar3)(uVar12,uVar13,uVar14);
  puVar6 = PTR_DAT_0002277c;
  puVar5 = PTR_FUN_00022760;
  *(undefined2 *)(puVar4 + 0xc) = uVar7;
  uVar13 = (*(code *)puVar5)(puVar6);
  uVar7 = (*(code *)puVar3)(uVar13,DAT_00022780,uVar14);
  *(undefined2 *)(puVar4 + 0xe) = uVar7;
  if (cVar8 == '\0') {
    puVar4[0x10] = *PTR_DAT_00022784;
  }
  else {
    puVar4[0x10] = 0;
  }
  cVar10 = (*(code *)puVar1)(PTR_DAT_00022788);
  if (cVar10 == '\x01') {
    puVar4[0x11] = puVar4[0x11] | 1;
  }
  else {
    puVar4[0x11] = puVar4[0x11] & 0xfe;
  }
  if (*PTR_Control_SerialEnableOutput_0002278c == '\x01') {
    puVar4[0x11] = puVar4[0x11] | 2;
  }
  else {
    puVar4[0x11] = puVar4[0x11] & 0xfd;
  }
  if (*PTR_Control_QualifiedSerialFeedback_00022790 == '\x01') {
    puVar4[0x11] = puVar4[0x11] | 4;
  }
  else {
    puVar4[0x11] = puVar4[0x11] & 0xfb;
  }
  if (*PTR_DAT_00022794 == '\x01') {
    puVar4[0x11] = puVar4[0x11] | 8;
  }
  else {
    puVar4[0x11] = puVar4[0x11] & 0xf7;
  }
  if (cVar9 == '\x01') {
    puVar4[0x11] = puVar4[0x11] | 0x10;
  }
  else {
    puVar4[0x11] = puVar4[0x11] & 0xef;
  }
  cVar9 = (*(code *)PTR_Protected_ReadByteOrDefault_0002279c)(PTR_DAT_00022798,0);
  if (cVar9 == '\x01') {
    puVar4[0x11] = puVar4[0x11] | 0x20;
  }
  else {
    puVar4[0x11] = puVar4[0x11] & 0xdf;
  }
  cVar9 = (*(code *)puVar1)(PTR_Control_FeedbackOverrideEnabled_000227a0);
  if (cVar9 == '\x01') {
    puVar4[0x11] = puVar4[0x11] | 0x40;
  }
  else {
    puVar4[0x11] = puVar4[0x11] & 0xbf;
  }
  if (*PTR_DAT_000228c4 == '\x01') {
    puVar4[0x11] = puVar4[0x11] | 0x80;
  }
  else {
    puVar4[0x11] = puVar4[0x11] & 0x7f;
  }
  pbVar11 = puVar4 + 0x12;
  if (*PTR_DAT_000228c8 == '\x01') {
    *pbVar11 = *pbVar11 | 1;
  }
  else {
    *pbVar11 = *pbVar11 & 0xfe;
  }
  pbVar11 = puVar4 + 0x12;
  if (cVar8 == '\0') {
    if (*PTR_DAT_000228cc == '\x01') {
      *pbVar11 = *pbVar11 | 2;
    }
    else {
      *pbVar11 = *pbVar11 & 0xfd;
    }
    if ((*PTR_DAT_000228d0 == '\0') && (*PTR_DAT_000228d4 == '\0')) {
      if (*PTR_DAT_000228d8 == '\x01') {
        puVar4[0x12] = puVar4[0x12] | 4;
      }
      else {
        puVar4[0x12] = puVar4[0x12] & 0xfb;
      }
    }
    else {
      puVar4[0x12] = puVar4[0x12] & 0xfb;
    }
  }
  else {
    *pbVar11 = *pbVar11 & 0xfd;
    puVar4[0x12] = puVar4[0x12] & 0xfb;
  }
  pbVar11 = puVar4 + 0x12;
  if (*puVar2 == '\x01') {
    *pbVar11 = *pbVar11 | 8;
  }
  else {
    *pbVar11 = *pbVar11 & 0xf7;
  }
  puVar1 = PTR_DAT_000228e0;
  puVar4[0x13] = *PTR_DAT_000228dc;
  *(undefined2 *)(puVar4 + 0x14) = *(undefined2 *)puVar1;
  *(undefined2 *)(puVar4 + 0x16) = *DAT_000228e4;
  return;
}

