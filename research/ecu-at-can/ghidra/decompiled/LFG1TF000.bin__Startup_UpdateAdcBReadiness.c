/* Ghidra analysis output; verify against original SH instructions. */

/* 12544 independentwholeRAM cases
   PASS:descriptor5C57C/F812,completionF818,14128count,16FF6conversion->84DC/84DA. State1 high>5547
   andstate2 high>9000 eachrequireunsigned100000timestampcounts beforeadvance; zeroisunsetmarker.
   Otherstates unchanged. F6C0/ADC explicit,no sensorunits/bootclaim. tcu-readiness-b.txt. */

uint Startup_UpdateAdcBReadiness(void)

{
  undefined *puVar1;
  undefined *puVar2;
  char cVar5;
  uint uVar3;
  ushort uVar4;
  ushort *puVar6;
  uint uVar7;
  byte bVar8;
  uint *puVar9;
  undefined1 auStack_18 [8];
  
  puVar2 = PTR_DAT_00011ed0;
  puVar1 = PTR_FUN_00011ecc;
  bVar8 = *PTR_Startup_AdcBReadinessState_00011ec8;
  cVar5 = (*(code *)PTR_FUN_00011ecc)(PTR_DAT_00011ed0);
  while (cVar5 != '\x01') {
    cVar5 = (*(code *)puVar1)(puVar2);
  }
  uVar3 = (*(code *)PTR_OutputHandoff_ReadAdcCount_00011ed4)(puVar2);
  puVar1 = PTR_OutputCycle_ConvertInputA_00011ed8;
  *(uint *)(int)DAT_00011ec0 = uVar3 & 0xffff;
  uVar4 = (*(code *)puVar1)(uVar3 & 0xffff,auStack_18);
  puVar1 = PTR_OutputTask_ReadTimestamp_00011edc;
  puVar6 = (ushort *)(int)DAT_00011eba;
  *puVar6 = uVar4;
  uVar3 = (uint)bVar8;
  uVar7 = (uint)*puVar6;
  if (uVar3 == 1) {
    puVar9 = (uint *)(int)DAT_00011ebc;
    if ((int)uVar7 <= (int)DAT_00011ec2) {
      *puVar9 = 0;
      goto LAB_00011ea8;
    }
    if (*puVar9 != 0) {
      uVar3 = (*(code *)puVar1)();
      if (PTR_LAB_00011ee0 <= (undefined *)(uVar3 - *puVar9)) {
        *puVar9 = 0;
        bVar8 = 2;
      }
      goto LAB_00011ea8;
    }
  }
  else {
    if (uVar3 != 2) goto LAB_00011ea8;
    puVar9 = (uint *)(int)DAT_00011ebe;
    if ((int)uVar7 <= (int)DAT_00011ec4) {
      *puVar9 = 0;
      goto LAB_00011ea8;
    }
    if (*puVar9 != 0) {
      uVar3 = (*(code *)puVar1)();
      if (PTR_LAB_00011ee0 <= (undefined *)(uVar3 - *puVar9)) {
        *puVar9 = 0;
        bVar8 = 3;
      }
      goto LAB_00011ea8;
    }
  }
  uVar3 = (*(code *)puVar1)();
  *puVar9 = uVar3;
LAB_00011ea8:
  *PTR_Startup_AdcBReadinessState_00011ec8 = bVar8;
  return uVar3;
}

