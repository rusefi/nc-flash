/* Ghidra analysis output; verify against original SH instructions. */

/* 402 tests: holdbit0 if historysum<=91643 and elapsed91AC ratio>538; otherwise
   clears8158.8158>=244 setsbits1/2 andreset. Low809A/nonzero8080/index0 clearsbit1.9194bit0
   ORs91A6bit1,92C6bit1,AC87. See tcu-reference-source.txt. */

void Reference_UpdateHoldAndFaultGates(void)

{
  undefined *puVar1;
  uint uVar2;
  uint uVar3;
  byte bVar4;
  byte *pbVar5;
  
  uVar2 = Reference_SumCaptureHistory((int)DAT_00020d0c);
  uVar3 = (*(code *)PTR_FUN_00020d28)
                    ((uint)*(ushort *)(int)DAT_00020d10 << 0x10,
                     *(uint *)(PTR_Reference_CaptureHistory_00020d24 +
                              (uint)*(byte *)(int)DAT_00020d0e * 4) >> 2);
  puVar1 = PTR_Reference_HoldTimer_00020d2c;
  pbVar5 = (byte *)(int)DAT_00020d0a;
  if ((*(uint *)PTR_DAT_00020d30 < uVar2) || (uVar3 <= *(ushort *)PTR_DAT_00020d34)) {
    *pbVar5 = *pbVar5 & 0xfe;
    *puVar1 = 0;
  }
  else {
    *pbVar5 = *pbVar5 | 1;
  }
  if ((byte)*PTR_DAT_00020e1c <= (byte)*puVar1) {
    *pbVar5 = *pbVar5 | 2;
    *pbVar5 = *pbVar5 | 4;
    Reference_ResetCaptureHistory();
  }
  if (((DAT_ffff809a < *(short *)PTR_DAT_00020e20) && (TransmissionStateClass != 0)) &&
     (CAN231_SixStateSource == 0)) {
    *pbVar5 = *pbVar5 & 0xfd;
  }
  if ((((*pbVar5 & 2) == 0) && ((*PTR_ApplicationFaultFlags92C6_00020e28 & 2) == 0)) &&
     (*PTR_DAT_00020e2c == '\0')) {
    bVar4 = *PTR_Reference_SourceStatus_00020e24 & 0xfe;
  }
  else {
    bVar4 = *PTR_Reference_SourceStatus_00020e24 | 1;
  }
  *PTR_Reference_SourceStatus_00020e24 = bVar4;
  return;
}

