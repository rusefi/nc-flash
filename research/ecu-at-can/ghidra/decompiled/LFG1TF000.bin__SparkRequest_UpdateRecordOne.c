/* Ghidra analysis output; verify against original SH instructions. */

/* 2C30C admission; active9530bit0 calls2C43A/2C400; stores953A and9542bit0 through1FB4A(index1),
   otherwise resets record/phase.900 full phase3 caller cases and5 paired CAN216/ECU lifecycle
   samples. Entry phase1/2 unproved. */

void SparkRequest_UpdateRecordOne(void)

{
  undefined *puVar1;
  char cVar3;
  byte bVar4;
  short sVar2;
  undefined1 *puVar5;
  byte *pbVar6;
  undefined2 *puVar7;
  short *psVar8;
  
  puVar1 = PTR_DAT_0002c2f8;
  bVar4 = *PTR_DAT_0002c2f8 & 1;
  cVar3 = SparkRequest_CheckRecordOneAdmission();
  if (cVar3 == '\x01') {
    if (bVar4 == 0) {
      bVar4 = FUN_0002c370();
    }
  }
  else {
    bVar4 = 0;
  }
  psVar8 = (short *)(int)DAT_0002c2f0;
  if (bVar4 == 1) {
    sVar2 = SparkRequest_CalculateRecordOneValue();
    *psVar8 = sVar2;
    bVar4 = SparkRequest_CheckRecordOneContinuation();
  }
  if (bVar4 == 1) {
    (*(code *)PTR_SparkRequest_SetRecord_0002c2fc)(1,(int)*psVar8,*(byte *)(int)DAT_0002c2f2 & 1);
  }
  else {
    sVar2 = (*(code *)PTR_FUN_0002c304)();
    pbVar6 = (byte *)(int)DAT_0002c2f2;
    *psVar8 = sVar2;
    puVar5 = (undefined1 *)(int)DAT_0002c2ee;
    *pbVar6 = *pbVar6 & 0xfe;
    *puVar5 = 0;
    (*(code *)PTR_SparkRequest_ResetRecord_0002c308)(1);
  }
  if (bVar4 == 0) {
    bVar4 = *puVar1 & 0xfe;
  }
  else {
    bVar4 = *puVar1 | 1;
  }
  *puVar1 = bVar4;
  puVar7 = (undefined2 *)(int)DAT_0002c2f4;
  puVar7[3] = puVar7[2];
  puVar7[2] = puVar7[1];
  puVar7[1] = *puVar7;
  *puVar7 = Phase_MeasuredSourceSample;
  return;
}

