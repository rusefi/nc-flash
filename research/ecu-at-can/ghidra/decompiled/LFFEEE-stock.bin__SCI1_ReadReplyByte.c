/* Ghidra analysis output; verify against original SH instructions. */

/* ExplicitRDR1 F00D sample to4352+index;first38bytes accumulate43A4. Sampledperipheral
   verification. */

byte SCI1_ReadReplyByte(byte param_1)

{
  byte bVar1;
  undefined4 local_10;
  byte bStack_c;
  
  bStack_c = param_1;
  (*(code *)PTR_FUN_0000c5b8)(&local_10,(int)DAT_0000c5a8);
  bVar1 = *(byte *)(int)DAT_0000c5aa;
  *(byte *)(int)DAT_0000c5ac = *(byte *)(int)DAT_0000c5ac & 0xbf | 0xb8;
  (*(code *)PTR_FUN_0000c5bc)(local_10);
  PTR_SCI1_ReplyBuffer_0000c5c0[bStack_c] = bVar1;
  if (bStack_c < 0x26) {
    *(ushort *)PTR_SCI1_ReceiveByteSum_0000c5c4 =
         *(short *)PTR_SCI1_ReceiveByteSum_0000c5c4 + (ushort)bVar1;
  }
  return bStack_c;
}

