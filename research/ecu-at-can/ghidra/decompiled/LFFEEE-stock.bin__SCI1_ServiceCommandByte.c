/* Ghidra analysis output; verify against original SH instructions. */

/* Activeexchange41calls:send0,thenreceiveprevious/sendnext through39,receive39/finishat40. Explicit
   callbacks,notinterrupttiming;control-serial.txt. */

void SCI1_ServiceCommandByte(void)

{
  byte bVar1;
  undefined *puVar2;
  int iVar3;
  
  puVar2 = PTR_SCI1_ExchangeByteIndex_0000c05c;
  if (*PTR_SCI1_ExchangeActive_0000c054 == '\0') {
    return;
  }
  *PTR_DAT_0000c058 = 0;
  bVar1 = *puVar2;
  if (bVar1 == 0) {
    iVar3 = 0;
  }
  else {
    if (0x27 < bVar1) {
      SCI1_ReadReplyByte((int)DAT_0000c036 + (int)(char)bVar1);
      SCI1_FinishAndCheckReply();
      goto LAB_0000bffc;
    }
    SCI1_ReadReplyByte((int)DAT_0000c036 + (int)(char)bVar1);
    iVar3 = (int)(char)*puVar2;
  }
  SCI1_SendCommandByte(iVar3);
LAB_0000bffc:
  *puVar2 = *puVar2 + '\x01';
  return;
}

