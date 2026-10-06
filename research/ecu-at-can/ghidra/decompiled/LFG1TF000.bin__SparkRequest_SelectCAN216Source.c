/* Ghidra analysis output; verify against original SH instructions. */

/* WARNING: Removing unreachable block (ram,0x0001fc70) */
/* WARNING: Removing unreachable block (ram,0x0001fc28) */
/* WARNING: Removing unreachable block (ram,0x0001fc94) */
/* Stock5CD0C enables slots1/2; later nonsentinel value/mode selected independently. Ignore local
   slot2zero when slot1present. Mode1 givesmax(signed16(92E4-selected),0),else7FFF
   ->915A;80BE=-selected,9158bit0=mode!=0.4900 cases plus paired ramp; see tcu-spark-requests.txt.
    */

void SparkRequest_SelectCAN216Source(void)

{
  undefined *puVar1;
  short sVar3;
  short sVar4;
  char cVar6;
  short sVar5;
  undefined4 uVar2;
  byte bVar7;
  int extraout_r3;
  int iVar8;
  int iVar9;
  int iVar10;
  int iVar11;
  undefined1 local_34 [8];
  short local_2c [8];
  
  puVar1 = PTR_SparkRequest_RecordEnableTable_0001fc24;
  iVar8 = (int)DAT_0001fc00;
  iVar9 = (int)DAT_0001fc04;
  iVar10 = 0;
  do {
    if (puVar1[iVar10] == '\0') {
      SparkRequest_ResetRecord(iVar10);
    }
    local_2c[iVar10] = *(short *)(iVar8 + iVar10 * 2);
    iVar11 = iVar10 + 1;
    local_34[iVar10] = *(undefined1 *)(iVar9 + iVar10);
    iVar10 = iVar11;
  } while (iVar11 < 5);
  if ((local_2c[2] == 0) && (local_2c[1] != DAT_0001fbfe)) {
    local_2c[2] = DAT_0001fbfe;
    local_34[2] = (undefined1)DAT_0001fc02;
  }
  sVar3 = (*(code *)PTR_FUN_0001fd00)();
  sVar4 = (*(code *)PTR_Request_SelectLastWord_0001fd04)(local_2c,5,(int)sVar3);
  cVar6 = (*(code *)PTR_Request_SelectLastByte_0001fd08)(local_34,5,0);
  sVar3 = DAT_0001fcf6;
  if (cVar6 == '\x01') {
    sVar3 = *(short *)PTR_SparkRequest_BaseValue_0001fd0c - sVar4;
  }
  sVar5 = (*(code *)PTR_FUN_0001fd00)();
  if (extraout_r3 < sVar5) {
    sVar3 = (*(code *)PTR_FUN_0001fd00)();
  }
  uVar2 = (*(code *)PTR_FUN_0001fd14)();
  if (cVar6 == '\0') {
    bVar7 = *PTR_SparkRequest_SelectedModeFlags_0001fd18 & 0xfe;
  }
  else {
    bVar7 = *PTR_SparkRequest_SelectedModeFlags_0001fd18 | 1;
  }
  *PTR_SparkRequest_SelectedModeFlags_0001fd18 = bVar7;
  puVar1 = PTR_FUN_0001fd20;
  SparkRequest_NegatedSelectedReduction = -sVar4;
  *(short *)PTR_CAN216_NumericRequestSource_0001fd1c = sVar3;
  (*(code *)puVar1)(uVar2);
  return;
}

