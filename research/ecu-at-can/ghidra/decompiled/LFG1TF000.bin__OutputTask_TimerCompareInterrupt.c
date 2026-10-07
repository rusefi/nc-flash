/* Ghidra analysis output; verify against original SH instructions. */

/* Executed entry through169A0 beforeRTE. F62Cbit0
   gatesack/87F4increment/F604=4166*(2*(phase&3)+1)/1227Efulltask. Profilinghelpers and
   registerrestore execute; no hardwaredelivery/RTE. See tcu-output-task.txt. */

undefined8 OutputTask_TimerCompareInterrupt(void)

{
  short sVar1;
  undefined *puVar2;
  undefined4 in_r0;
  undefined4 in_r1;
  ushort *puVar3;
  byte *pbVar4;
  
  (*(code *)PTR_OutputTask_RecordInterruptEntry_00016a24)
            (10,(int)*(short *)(int)DAT_00016a12 - (int)*(short *)(int)DAT_00016a16);
  puVar3 = (ushort *)(int)DAT_00016a1a;
  if ((*puVar3 & 1) != 0) {
    *puVar3 = *puVar3 & (ushort)PTR_DAT_00016a28;
    puVar2 = PTR_OutputTask_CompareCallback_00016a2c;
    sVar1 = DAT_00016a14;
    pbVar4 = (byte *)(int)DAT_00016a18;
    *pbVar4 = *pbVar4 + 1;
    *(ushort *)(int)DAT_00016a16 = ((*pbVar4 & 3) * 2 + 1) * sVar1;
    (*(code *)puVar2)();
  }
  (*(code *)PTR_OutputTask_RecordInterruptExit_00016a30)(10);
  return CONCAT44(in_r1,in_r0);
}

