/* Ghidra analysis output; verify against original SH instructions. */

/* Requires8F6C bit08. Consumes per-field freshness via1C018, refreshes record deadline/recovery or
   checks expiry. Ten record lifecycles verified. */

uint CAN_UpdateReceiveDeadlines(void)

{
  undefined *puVar1;
  byte bVar3;
  char cVar4;
  uint uVar2;
  
  bVar3 = (*(code *)PTR_FUN_00019ba0)();
  puVar1 = PTR_CAN_ConsumeFieldFreshness_00019ba4;
  uVar2 = (uint)((bVar3 & 8) != 0);
  if (uVar2 != 1) {
    return uVar2;
  }
  cVar4 = (*(code *)PTR_CAN_ConsumeFieldFreshness_00019ba4)(0x2e);
  if (cVar4 == '\0') {
    CAN_CheckReceiveRecordExpiry(0);
  }
  else {
    CAN_SetRecordDeadline(0);
    CAN_ReceiveRecordRecovery(0);
  }
  cVar4 = (*(code *)puVar1)(0x2c);
  if (cVar4 == '\0') {
    CAN_CheckReceiveRecordExpiry(1);
  }
  else {
    CAN_SetRecordDeadline(1,0);
    CAN_ReceiveRecordRecovery(1);
  }
  cVar4 = (*(code *)puVar1)(0x2b);
  if (cVar4 == '\0') {
    CAN_CheckReceiveRecordExpiry(2);
  }
  else {
    CAN_SetRecordDeadline(2,0);
    CAN_ReceiveRecordRecovery(2);
  }
  cVar4 = (*(code *)puVar1)(0x1f);
  if (cVar4 == '\0') {
    CAN_CheckReceiveRecordExpiry(3);
  }
  else {
    CAN_SetRecordDeadline(3,0);
    CAN_ReceiveRecordRecovery(3);
  }
  cVar4 = (*(code *)puVar1)(0x18);
  if (cVar4 == '\0') {
    CAN_CheckReceiveRecordExpiry(7);
  }
  else {
    CAN_SetRecordDeadline(7,0);
    CAN_ReceiveRecordRecovery(7);
  }
  cVar4 = (*(code *)puVar1)(0x17);
  if (cVar4 == '\0') {
    CAN_CheckReceiveRecordExpiry(8);
  }
  else {
    CAN_SetRecordDeadline(8,0);
    CAN_ReceiveRecordRecovery(8);
  }
  cVar4 = (*(code *)puVar1)(0x16);
  if (cVar4 == '\0') {
    CAN_CheckReceiveRecordExpiry(9);
  }
  else {
    CAN_SetRecordDeadline(9,0);
    CAN_ReceiveRecordRecovery(9);
  }
  cVar4 = (*(code *)puVar1)(0x12);
  if (cVar4 == '\0') {
    CAN_CheckReceiveRecordExpiry(10);
  }
  else {
    CAN_SetRecordDeadline(10,0);
    CAN_ReceiveRecordRecovery(10);
  }
  cVar4 = (*(code *)puVar1)(6);
  if (cVar4 == '\0') {
    CAN_CheckReceiveRecordExpiry(0xc);
  }
  else {
    CAN_SetRecordDeadline(0xc,0);
    CAN_ReceiveRecordRecovery(0xc);
  }
  cVar4 = (*(code *)puVar1)(0);
  if (cVar4 != '\0') {
    CAN_SetRecordDeadline(0xd,0);
    uVar2 = CAN_ReceiveRecordRecovery(0xd);
    return uVar2;
  }
  uVar2 = CAN_CheckReceiveRecordExpiry(0xd);
  return uVar2;
}

