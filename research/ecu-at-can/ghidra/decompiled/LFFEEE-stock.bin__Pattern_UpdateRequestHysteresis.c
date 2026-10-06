/* Ghidra analysis output; verify against original SH instructions. */

/* 715C versus712C/7130/7134 with stock hysteresis5;7188/89/8A hold at lower equality.718B uses0.75
   plus1/128 deadband.567 cases. */

uint Pattern_UpdateRequestHysteresis(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined1 uVar4;
  uint uVar3;
  float fVar5;
  
  puVar1 = PTR_DAT_0003fc1c;
  fVar5 = *(float *)PTR_DAT_0003fbd0;
  uVar4 = Pattern_Hysteresis(fVar5,*(undefined4 *)PTR_DAT_0003fc20,*(undefined4 *)PTR_DAT_0003fc1c,
                             (int)(char)*PTR_Pattern_UpperThresholdLatch_0003fc24);
  *PTR_Pattern_UpperThresholdLatch_0003fc24 = uVar4;
  uVar4 = Pattern_Hysteresis(fVar5,*(undefined4 *)PTR_DAT_0003fc28,*(undefined4 *)puVar1,
                             (int)(char)*PTR_Pattern_MiddleThresholdLatch_0003fc2c);
  puVar2 = PTR_DAT_0003fc30;
  *PTR_Pattern_MiddleThresholdLatch_0003fc2c = uVar4;
  uVar4 = Pattern_Hysteresis(fVar5,*(undefined4 *)puVar2,*(undefined4 *)puVar1,
                             (int)(char)*PTR_Pattern_LowerThresholdLatch_0003fc34);
  puVar1 = PTR_DAT_0003fc38;
  *PTR_Pattern_LowerThresholdLatch_0003fc34 = uVar4;
  uVar3 = (*(code *)PTR_FUN_0003fbcc)(fVar5,*(undefined4 *)puVar1,DAT_0003fc3c);
  if ((fVar5 <= *(float *)puVar1) || ((uVar3 & 0xff) == 0)) {
    *PTR_Pattern_MinimumRequestFlag_0003fc40 = 0;
  }
  else if (*(float *)puVar1 < fVar5) {
    *PTR_Pattern_MinimumRequestFlag_0003fc40 = 1;
  }
  return uVar3;
}

