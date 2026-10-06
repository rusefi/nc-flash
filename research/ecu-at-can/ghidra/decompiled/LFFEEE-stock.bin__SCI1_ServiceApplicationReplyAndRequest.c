/* Ghidra analysis output; verify against original SH instructions. */

/* Fullreceipt/header/command/scheduling execution:810 header/status,120 scheduling cases.
   Invalidreply retainsnumericfeedback;control-reply.txt. Localmodes0/1,6DF8=0;resetC260 branchopen.
    */

char SCI1_ServiceApplicationReplyAndRequest(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  char cVar4;
  undefined2 uVar5;
  char cVar6;
  undefined1 uVar7;
  uint uVar8;
  byte bVar9;
  undefined2 *puVar10;
  undefined *puVar11;
  int iVar12;
  ushort *puVar13;
  uint uVar14;
  undefined4 local_3c;
  undefined4 uStack_38;
  undefined4 uStack_34;
  undefined4 uStack_30;
  undefined4 uStack_2c;
  char local_28;
  char local_24;
  
  local_24 = (*(code *)PTR_FUN_000222a0)(PTR_DAT_0002229c);
  puVar11 = PTR_Register_UpdateMaskedWord_000222ac;
  puVar2 = PTR_FUN_000222a8;
  puVar1 = PTR_FUN_000222a4;
  puVar13 = (ushort *)(int)DAT_00022296;
  iVar12 = (int)DAT_00022298;
  if ((*puVar13 & 4) == 0) {
    (*(code *)PTR_FUN_000222a4)(&uStack_2c,iVar12);
    (*(code *)puVar11)(puVar13,8,0);
    (*(code *)puVar2)(uStack_2c);
    (*(code *)puVar1)(&uStack_30,iVar12);
    (*(code *)puVar11)(puVar13,4,1);
    (*(code *)puVar2)(uStack_30);
  }
  else if ((*puVar13 & 8) == 0) {
    (*(code *)PTR_FUN_000222a4)(&uStack_34,iVar12);
    (*(code *)puVar11)(puVar13,8,1);
    (*(code *)puVar2)(uStack_34);
  }
  puVar3 = PTR_DAT_000223b8;
  *PTR_SCI1_ApplicationFeedbackReceived_000223b4 = 0;
  *puVar3 = 0;
  (*(code *)puVar1)(&uStack_38,iVar12);
  (*(code *)puVar11)((int)DAT_000223b0,(int)DAT_000223ae,*PTR_DAT_000223b8 == '\x01');
  (*(code *)puVar2)(uStack_38);
  (*(code *)puVar1)(&local_3c,iVar12);
  local_28 = (*(code *)PTR_SCI1_ConsumeExchangeStatus_000223bc)();
  (*(code *)puVar2)(local_3c);
  cVar4 = local_28;
  puVar2 = PTR_SCI1_ApplicationReplyRecord_000223c4;
  puVar1 = PTR_SCI1_ReadReplyWord_000223c0;
  if (local_28 == '\x01') {
    uVar5 = (*(code *)PTR_SCI1_ReadReplyWord_000223c0)(0);
    *(undefined2 *)puVar2 = uVar5;
    uVar5 = (*(code *)puVar1)(1);
    *(undefined2 *)(puVar2 + 2) = uVar5;
    puVar11 = (undefined *)(uint)*(ushort *)puVar2;
    if (puVar11 == (undefined *)(uint)(ushort)~*(ushort *)(puVar2 + 2)) {
      uVar14 = 2;
      do {
        uVar8 = uVar14 & 0xff;
        uVar5 = (*(code *)puVar1)(uVar14);
        uVar14 = uVar14 + 1;
        *(undefined2 *)(puVar2 + uVar8 * 2) = uVar5;
      } while ((uVar14 & 0xff) < 0x13);
      if (((DAT_000223c8 <= (int)puVar11) && ((int)puVar11 <= (int)PTR_PTR_000223cc)) ||
         (puVar11 == PTR_LAB_000223d0)) {
        SCI1_DecodeApplicationFeedback();
        *PTR_SCI1_ApplicationFeedbackReceived_000223b4 = 1;
      }
      if ((DAT_000223c8 <= (int)puVar11) && ((int)puVar11 <= (int)PTR_PTR_000223cc)) {
        SCI1_CopyReplyCalibrationWords(((int)*(short *)puVar2 + (int)DAT_000223b2) * 4,0xf);
      }
      (*(code *)PTR_FUN_000223d4)();
    }
    *(float *)PTR_DAT_000223e4 =
         *(float *)PTR_DAT_000223d8 +
         *(float *)PTR_SCI1_SecondaryFeedbackValue_000223e0 * *(float *)PTR_DAT_000223dc;
  }
  cVar6 = (*(code *)PTR_FUN_000224a8)();
  puVar1 = PTR_DAT_000224ac;
  if (cVar6 == '\x01') {
    uVar7 = (*(code *)PTR_FUN_000224b0)((int)(char)*PTR_DAT_000224ac,1);
    *puVar1 = uVar7;
  }
  else {
    *PTR_DAT_000224ac = 0;
  }
  puVar2 = PTR_SCI1_OutgoingSequence_000224c0;
  puVar1 = PTR_Control_OutgoingCommandRecord_000224b8;
  if (((cVar4 == '\x01') || (cVar4 == '\x02')) ||
     ((byte)*PTR_DAT_000224b4 < (byte)*PTR_DAT_000224ac)) {
    if (cVar6 == '\x01') {
      *(short *)PTR_Control_OutgoingCommandRecord_000224b8 = (short)PTR_LAB_000224bc;
      *(undefined2 *)(puVar1 + 2) = DAT_000224a4;
      FUN_000228a2();
    }
    else {
      *(undefined2 *)PTR_Control_OutgoingCommandRecord_000224b8 =
           *(undefined2 *)PTR_SCI1_OutgoingSequence_000224c0;
      *(ushort *)(puVar1 + 2) = ~*(ushort *)puVar2;
      Control_PackOutgoingCommandRecord();
      bVar9 = 0xf;
      iVar12 = 0x1e;
      puVar10 = (undefined2 *)(PTR_DAT_000224c8 + (int)(PTR_DAT_000224c4 + *(ushort *)puVar1) * 8);
      do {
        uVar5 = *puVar10;
        puVar10 = puVar10 + 1;
        bVar9 = bVar9 + 1;
        *(undefined2 *)(puVar1 + iVar12) = uVar5;
        iVar12 = iVar12 + 2;
      } while (bVar9 < 0x13);
      if ((int)(uint)*(ushort *)puVar2 < (int)PTR_LAB_000224cc) {
        *(short *)puVar2 = *(short *)puVar2 + 1;
      }
      else {
        *(short *)puVar2 = (short)DAT_000224d0;
      }
    }
    puVar2 = PTR_DAT_000224d4;
    if (cVar6 == '\x01') {
      uVar7 = (*(code *)PTR_FUN_000224b0)((int)(char)*PTR_DAT_000224d4,1);
      *puVar2 = uVar7;
    }
    else {
      *PTR_DAT_000224d4 = 0;
    }
    puVar2 = PTR_Control_WriteOutgoingIndexedWord_0002271c;
    uVar14 = 0;
    do {
      (*(code *)puVar2)(uVar14,(int)*(short *)(puVar1 + (uVar14 & 0xff) * 2));
      uVar14 = uVar14 + 1;
    } while ((uVar14 & 0xff) < 0x13);
    (*(code *)PTR_SCI1_StartCommandExchange_00022720)();
  }
  cVar4 = local_24;
  if ((local_24 == '\x01') && (*PTR_DAT_00022724 == '\0')) {
    cVar6 = (*(code *)PTR_FUN_0002272c)(PTR_DAT_00022728);
    if (cVar6 == '\x01') {
      (*(code *)PTR_FUN_00022730)();
      FUN_000231f8();
    }
  }
  else {
    cVar6 = (*(code *)PTR_FUN_00022734)();
    if (cVar6 == '\x01') {
      (*(code *)PTR_FUN_00022730)();
    }
  }
  if (cVar4 == '\x01') {
    *PTR_DAT_00022724 = 1;
  }
  else {
    *PTR_DAT_00022724 = 0;
  }
  return cVar4;
}

