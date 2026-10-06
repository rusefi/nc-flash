/* Ghidra analysis output; verify against original SH instructions. */

/* Fullbodyexecuted;192 independentnumeric and192 sixchannelmajority checks.55DF1
   alternateconversion/directflags,elsewordangleconversion/majority.
   Otherflags/diagnosticsnotfullymodeled. */

void SCI1_DecodeApplicationFeedback(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined *puVar5;
  undefined *puVar6;
  undefined *puVar7;
  char cVar8;
  undefined4 in_r7;
  undefined4 uVar9;
  undefined4 uVar10;
  undefined4 uVar11;
  float fVar12;
  undefined4 uVar13;
  
  puVar2 = PTR_FUN_000229bc;
  puVar1 = PTR_SCI1_ApplicationReplyRecord_000229b4;
  uVar13 = 0;
  uVar11 = DAT_000229b8;
  uVar9 = (*(code *)PTR_FUN_000229bc)
                    (DAT_000229b8,0,(int)*(short *)(PTR_SCI1_ApplicationReplyRecord_000229b4 + 8));
  *(undefined4 *)PTR_DAT_000229c0 = uVar9;
  uVar9 = (*(code *)puVar2)(uVar11,uVar13,(int)*(short *)(puVar1 + 10));
  *(undefined4 *)PTR_DAT_000229c4 = uVar9;
  if (*PTR_DAT_000229c8 == '\x01') {
    fVar12 = DAT_000229cc;
    uVar10 = (*(code *)PTR_FUN_000229dc)
                       (((*(float *)PTR_DAT_000229c0 - *(float *)PTR_DAT_000229d0) *
                         *(float *)PTR_DAT_000229d4 * DAT_000229d8) / DAT_000229cc,uVar13);
    uVar9 = (*(code *)PTR_FUN_000229dc)
                      (((*(float *)PTR_DAT_000229c4 - *(float *)PTR_DAT_000229e0) *
                        *(float *)PTR_DAT_000229e4 * DAT_000229d8) / fVar12,uVar13);
  }
  else {
    uVar9 = DAT_00022c44;
    uVar10 = (*(code *)puVar2)(DAT_00022c44,uVar13,(int)*(short *)(puVar1 + 4));
    uVar9 = (*(code *)puVar2)(uVar9,uVar13,(int)*(short *)(puVar1 + 6));
  }
  *(undefined4 *)PTR_SCI1_SecondaryFeedbackValue_00022c48 = uVar9;
  (*(code *)PTR_FUN_00022c50)(uVar10,PTR_SCI1_ProtectedFeedbackValue_00022c4c);
  uVar11 = (*(code *)puVar2)(uVar11,uVar13,(int)*(short *)(puVar1 + 0xc));
  *(undefined4 *)PTR_DAT_00022c54 = uVar11;
  uVar11 = (*(code *)PTR_FUN_00022c5c)(DAT_00022c58,uVar13,(int)(char)puVar1[0xe]);
  *(undefined4 *)PTR_DAT_00022c60 = uVar11;
  puVar4 = PTR_DAT_00022c74;
  puVar3 = PTR_DAT_00022c70;
  puVar2 = PTR_DAT_00022c6c;
  *(float *)PTR_DAT_00022c68 = (float)(int)(char)puVar1[0xf] * DAT_00022c64;
  *puVar2 = puVar1[0x10];
  puVar6 = PTR_DAT_00022c7c;
  puVar2 = PTR_DAT_00022c78;
  if (*PTR_DAT_00022c80 == '\x01') {
    *PTR_DAT_00022c70 = puVar1[0x11];
    puVar5 = PTR_DAT_00022c74;
    *puVar2 = puVar1[0x12];
    *puVar5 = puVar1[0x13];
    puVar5 = PTR_DAT_00022c84;
    *PTR_DAT_00022c7c = puVar1[0x14];
    puVar7 = PTR_DAT_00022c88;
    *puVar5 = puVar1[0x15];
    *puVar7 = puVar1[0x16];
  }
  else {
    SCI1_FilterReplyStatusByte
              ((int)(char)puVar1[0x11],(int)(char)*PTR_DAT_00022c8c,PTR_DAT_00022c70,in_r7,puVar3);
    SCI1_FilterReplyStatusByte
              ((int)(char)puVar1[0x12],(int)(char)*PTR_DAT_00022c90,PTR_DAT_00022c78,in_r7,puVar2);
    SCI1_FilterReplyStatusByte
              ((int)(char)puVar1[0x13],(int)(char)*PTR_DAT_00022c94,PTR_DAT_00022c74,in_r7,puVar4);
    SCI1_FilterReplyStatusByte
              ((int)(char)puVar1[0x14],(int)(char)*PTR_DAT_00022c98,PTR_DAT_00022c7c,in_r7,puVar6);
    SCI1_FilterReplyStatusByte
              ((int)(char)puVar1[0x15],(int)(char)*PTR_DAT_00022c9c,PTR_DAT_00022c84,in_r7,
               PTR_DAT_00022c84);
    SCI1_FilterReplyStatusByte
              ((int)(char)puVar1[0x16],(int)(char)*PTR_DAT_00022ca0,PTR_DAT_00022c88,in_r7,
               PTR_DAT_00022c88);
  }
  puVar5 = PTR_DAT_00022ca4;
  *PTR_DAT_00022c8c = puVar1[0x11];
  *PTR_DAT_00022c90 = puVar1[0x12];
  *PTR_DAT_00022c94 = puVar1[0x13];
  *PTR_DAT_00022c98 = puVar1[0x14];
  *PTR_DAT_00022c9c = puVar1[0x15];
  *PTR_DAT_00022ca0 = puVar1[0x16];
  if ((*puVar3 & 1) == 1) {
    *puVar5 = 1;
  }
  else {
    *puVar5 = 0;
  }
  if ((*puVar3 & 2) == 0) {
    *PTR_DAT_00022ca8 = 0;
  }
  else {
    *PTR_DAT_00022ca8 = 1;
  }
  (*(code *)PTR_FUN_00022cb0)(PTR_DAT_00022cac,(*puVar3 & 4) != 0);
  if ((*puVar3 & 8) == 0) {
    *PTR_DAT_00022cb4 = 0;
  }
  else {
    *PTR_DAT_00022cb4 = 1;
  }
  if ((*puVar3 & 0x20) == 0) {
    *PTR_DAT_00022cb8 = 0;
  }
  else {
    *PTR_DAT_00022cb8 = 1;
  }
  if (((int)(char)*puVar3 & 0x80U) == 0) {
    *PTR_DAT_00022cbc = 0;
  }
  else {
    *PTR_DAT_00022cbc = 1;
  }
  if ((*puVar2 & 2) == 0) {
    *PTR_DAT_00022cc0 = 0;
  }
  else {
    *PTR_DAT_00022cc0 = 1;
  }
  if ((*puVar2 & 8) == 0) {
    *PTR_DAT_00022cc4 = 0;
  }
  else {
    *PTR_DAT_00022cc4 = 1;
  }
  if ((*puVar2 & 0x20) == 0) {
    *PTR_DAT_00022cc8 = 0;
  }
  else {
    *PTR_DAT_00022cc8 = 1;
  }
  if (((int)(char)*puVar2 & 0x80U) == 0) {
    *PTR_DAT_00022ccc = 0;
  }
  else {
    *PTR_DAT_00022ccc = 1;
  }
  if (((*puVar4 & 2) == 0) || (*PTR_DAT_00022cd4 != '\x01')) {
    *PTR_DAT_00022cd0 = 0;
  }
  else {
    *PTR_DAT_00022cd0 = 1;
  }
  if ((*puVar4 & 8) == 0) {
    *PTR_DAT_00022ea4 = 0;
  }
  else {
    *PTR_DAT_00022ea4 = 1;
  }
  if ((*puVar4 & 0x20) == 0) {
    *PTR_DAT_00022ea8 = 0;
  }
  else {
    *PTR_DAT_00022ea8 = 1;
  }
  if (((int)(char)*puVar4 & 0x80U) == 0) {
    *PTR_DAT_00022eac = 0;
  }
  else {
    *PTR_DAT_00022eac = 1;
  }
  if ((*puVar6 & 2) == 0) {
    *PTR_DAT_00022eb0 = 0;
  }
  else {
    *PTR_DAT_00022eb0 = 1;
  }
  if (((*puVar6 & 8) == 0) && (*PTR_DAT_00022eb8 != '\0')) {
    *PTR_DAT_00022eb4 = 0;
  }
  else {
    *PTR_DAT_00022eb4 = 1;
  }
  if ((*puVar6 & 0x20) == 0) {
    *PTR_DAT_00022ebc = 0;
  }
  else {
    *PTR_DAT_00022ebc = 1;
  }
  if (((int)(char)*puVar6 & 0x80U) == 0) {
    *PTR_DAT_00022ec0 = 0;
  }
  else {
    *PTR_DAT_00022ec0 = 1;
  }
  if ((*PTR_DAT_00022ec8 & 2) == 0) {
    *PTR_DAT_00022ec4 = 0;
  }
  else {
    *PTR_DAT_00022ec4 = 1;
  }
  if ((*PTR_DAT_00022ec8 & 8) == 0) {
    *PTR_DAT_00022ecc = 0;
  }
  else {
    *PTR_DAT_00022ecc = 1;
  }
  if ((*PTR_DAT_00022ec8 & 0x20) == 0) {
    *PTR_DAT_00022ed0 = 0;
  }
  else {
    *PTR_DAT_00022ed0 = 1;
  }
  if (((int)(char)*PTR_DAT_00022ec8 & 0x80U) == 0) {
    *PTR_DAT_00022ed4 = 0;
  }
  else {
    *PTR_DAT_00022ed4 = 1;
  }
  puVar5 = PTR_FUN_00022ed8;
  if (*PTR_DAT_00022edc == '\x01') {
    cVar8 = (*(code *)PTR_Protected_ReadByteOrDefault_00022ee4)(PTR_DAT_00022ee0,1);
    if (cVar8 == '\x01') {
      (*(code *)puVar5)(PTR_DAT_00022ee8,0);
      (*(code *)puVar5)(PTR_DAT_00022eec,0);
      (*(code *)puVar5)(PTR_DAT_00022ef0,0);
      (*(code *)puVar5)(PTR_DAT_00022ef4,0);
      (*(code *)puVar5)(PTR_DAT_00022ef8,0);
      (*(code *)puVar5)(PTR_DAT_00022efc,0);
      (*(code *)puVar5)(PTR_DAT_00022f00,0);
      (*(code *)puVar5)(PTR_DAT_00022f04,0);
      (*(code *)puVar5)(PTR_DAT_00022f08,0);
      (*(code *)puVar5)(PTR_DAT_00022f0c,0);
      (*(code *)puVar5)(PTR_DAT_00022f10,0);
      (*(code *)puVar5)(PTR_DAT_00022f14,0);
      (*(code *)puVar5)(PTR_DAT_00022f18,0);
      (*(code *)puVar5)(PTR_DAT_00022f1c,0);
      (*(code *)puVar5)(PTR_DAT_00022f20,0);
      (*(code *)puVar5)(PTR_DAT_00022f24,0);
      (*(code *)puVar5)(PTR_DAT_00022f28,0);
      (*(code *)puVar5)(PTR_DAT_00022f2c,0);
      (*(code *)puVar5)(PTR_DAT_00022f30,0);
      (*(code *)puVar5)(PTR_DAT_00022f34,0);
    }
  }
  else {
    if ((*puVar3 & 0x10) != 0) {
      (*(code *)PTR_FUN_00022ed8)(PTR_DAT_00023178,1);
    }
    if ((*puVar3 & 0x40) != 0) {
      (*(code *)puVar5)(PTR_DAT_0002317c,1);
    }
    if ((*puVar2 & 1) == 1) {
      (*(code *)puVar5)(PTR_DAT_00023180,1);
    }
    if ((*puVar2 & 4) != 0) {
      (*(code *)puVar5)(PTR_DAT_00023184,1);
    }
    if ((*puVar2 & 0x10) != 0) {
      (*(code *)puVar5)(PTR_DAT_00023188,1);
    }
    if ((*puVar2 & 0x40) != 0) {
      (*(code *)puVar5)(PTR_DAT_0002318c,1);
    }
    if (((*puVar4 & 1) == 1) ||
       (cVar8 = (*(code *)PTR_Protected_ReadByteOrDefault_00023194)(PTR_DAT_00023190,0),
       cVar8 == '\x01')) {
      (*(code *)puVar5)(PTR_DAT_00023198,1);
    }
    if ((*puVar4 & 4) != 0) {
      (*(code *)puVar5)(PTR_DAT_0002319c,1);
    }
    if ((*puVar4 & 0x10) != 0) {
      (*(code *)puVar5)(PTR_DAT_000231a0,1);
    }
    if ((*puVar4 & 0x40) != 0) {
      (*(code *)puVar5)(PTR_DAT_000231a4,1);
    }
    if ((*puVar6 & 1) == 1) {
      (*(code *)puVar5)(PTR_DAT_000231a8,1);
    }
    if (*PTR_DAT_000231ac == '\0') {
      (*(code *)puVar5)(PTR_DAT_000231b0,0);
    }
    else if ((*puVar6 & 4) != 0) {
      (*(code *)puVar5)(PTR_DAT_000231b0,1);
    }
    if ((*puVar6 & 0x10) != 0) {
      (*(code *)puVar5)(PTR_DAT_000231b4,1);
    }
    if ((*puVar6 & 0x40) != 0) {
      (*(code *)puVar5)(PTR_DAT_000231b8,1);
    }
    if ((*PTR_DAT_000231bc & 1) == 1) {
      (*(code *)puVar5)(PTR_DAT_000231c0,1);
    }
    if ((*PTR_DAT_000231bc & 4) != 0) {
      (*(code *)puVar5)(PTR_DAT_000231c4,1);
    }
    if ((*PTR_DAT_000231bc & 0x10) != 0) {
      (*(code *)puVar5)(PTR_DAT_000231c8,1);
    }
    if ((*PTR_DAT_000231bc & 0x40) != 0) {
      (*(code *)puVar5)(PTR_DAT_000231cc,1);
    }
    if ((*PTR_DAT_000231d0 & 1) == 1) {
      (*(code *)puVar5)(PTR_DAT_000231d4,1);
    }
    if ((*PTR_DAT_000231d0 & 2) != 0) {
      (*(code *)puVar5)(PTR_DAT_000231d8,1);
    }
  }
  *PTR_DAT_000231dc = puVar1[0x17];
  *PTR_DAT_000231e0 = puVar1[0x18];
  *PTR_DAT_000231e4 = puVar1[0x19];
  *PTR_DAT_000231e8 = puVar1[0x1a];
  *PTR_DAT_000231ec = puVar1[0x1b];
  *PTR_DAT_000231f0 = puVar1[0x1c];
  *PTR_DAT_000231f4 = puVar1[0x1d];
  return;
}

