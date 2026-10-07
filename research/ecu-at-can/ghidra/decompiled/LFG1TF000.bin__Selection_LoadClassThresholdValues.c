/* Ghidra analysis output; verify against original SH instructions. */

/* 916Fbit2 selects one of two word columns at75138/34/30/2C/3C ->9C08/0A/0C/0E/10. Both stock
   columns equal4004,7542,11267,16013,21788. Original read-address audit verifies selector despite
   equal values. */

void Selection_LoadClassThresholdValues(void)

{
  undefined *puVar1;
  int iVar2;
  
  puVar1 = PTR_DAT_00047314;
  iVar2 = (-(((*PTR_Request_CancellationFlags_00047304 & 4) == 0) - 1) & 0xff) * 2;
  *(undefined2 *)PTR_DAT_0004730c =
       *(undefined2 *)(PTR_Selection_ClassThresholdCalibration_6__00047308 + iVar2);
  *(undefined2 *)puVar1 =
       *(undefined2 *)(PTR_Selection_ClassThresholdCalibration_4__00047310 + iVar2);
  *(undefined2 *)PTR_DAT_0004731c =
       *(undefined2 *)(PTR_Selection_ClassThresholdCalibration_2__00047318 + iVar2);
  *(undefined2 *)PTR_DAT_00047324 =
       *(undefined2 *)(PTR_Selection_ClassThresholdCalibration_00047320 + iVar2);
  *(undefined2 *)PTR_DAT_0004732c =
       *(undefined2 *)(PTR_Selection_ClassThresholdCalibration_8__00047328 + iVar2);
  return;
}

