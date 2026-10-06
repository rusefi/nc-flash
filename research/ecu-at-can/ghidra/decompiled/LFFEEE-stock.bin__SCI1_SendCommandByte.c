/* Ghidra analysis output; verify against original SH instructions. */

/* 437A bytes0..37 accumulate43A2;index38 writes BEchecksum5AA5-sum at43A0.40bytes reachTDR1 F00B.
    */

void SCI1_SendCommandByte(byte param_1)

{
  undefined *puVar1;
  byte bVar2;
  undefined4 local_10;
  uint uStack_c;
  
  puVar1 = PTR_Control_OutgoingWordBuffer_0000c498;
  uStack_c = (uint)param_1;
  bVar2 = PTR_Control_OutgoingWordBuffer_0000c498[uStack_c];
  if (param_1 < 0x26) {
    *(ushort *)PTR_SCI1_TransmitByteSum_0000c47c =
         *(short *)PTR_SCI1_TransmitByteSum_0000c47c + (ushort)bVar2;
  }
  else if (param_1 == 0x26) {
    *(short *)(PTR_Control_OutgoingWordBuffer_0000c498 + 0x26) =
         DAT_0000c468 - *(short *)PTR_SCI1_TransmitByteSum_0000c47c;
    bVar2 = puVar1[0x26];
  }
  (*(code *)PTR_FUN_0000c470)(&local_10,(int)DAT_0000c45c);
  *(byte *)(int)DAT_0000c46a = bVar2;
  *(byte *)(int)DAT_0000c460 = *(byte *)(int)DAT_0000c460 & 0x7f | 0x78;
  (*(code *)PTR_FUN_0000c474)(local_10);
  return;
}

