/* Ghidra analysis output; verify against original SH instructions. */

/* Unsigned32 timestamp delta/10 ->8908, calls211DC; clears88F0 and saturating
   increments8900/8902/8904.288 new timestamp/wrap cases connect history/measurement to shift
   lifecycle/CAN216. Earlier6001-call0722 test in speed-fault.txt; physical mapping open.
   Complete126EC experiment supplies5890 then6490 intervals, no age overrides; measured10865 at24
   ->9861 at71. See tcu-captured-requests.txt. Joined320 recovery pairs execute560
   originalcaptureISRprefixes with differentialRAM/register/MMIO checks; exactpriortrace
   afteronlynewobservations andcallbackPR normalization. See tcu-capture-delivery.txt; no
   hardwareadmission/cadence proof. */

undefined4 Capture0B_ProcessCapturedCount(int param_1)

{
  undefined *puVar1;
  uint uVar2;
  undefined4 uVar3;
  int iVar4;
  
  puVar1 = PTR_FUN_00017ad8;
  iVar4 = *(int *)(int)DAT_00017ac4;
  *(int *)(int)DAT_00017ac4 = param_1;
  uVar2 = (*(code *)puVar1)(param_1,param_1 - iVar4);
  puVar1 = PTR_Measurement_IngestCapture_00017ae0;
  if (DAT_00017adc < uVar2) {
    uVar2 = DAT_00017adc;
  }
  *(uint *)PTR_Measurement_CaptureDeltaDiv10_00017ad4 = uVar2;
  (*(code *)puVar1)();
  uVar3 = (*(code *)PTR_FUN_00017ae8)(PTR_DAT_00017ae4);
  puVar1 = PTR_DAT_00017aec;
  if ((undefined *)(uint)*(ushort *)PTR_SpeedFault_OtherCaptureCount_00017ac8 != PTR_DAT_00017aec) {
    *(short *)PTR_SpeedFault_OtherCaptureCount_00017ac8 =
         *(short *)PTR_SpeedFault_OtherCaptureCount_00017ac8 + 1;
  }
  if ((undefined *)(uint)*(ushort *)PTR_DAT_00017acc != puVar1) {
    *(short *)PTR_DAT_00017acc = *(short *)PTR_DAT_00017acc + 1;
  }
  if ((undefined *)(uint)*(ushort *)PTR_DAT_00017ad0 != puVar1) {
    *(short *)PTR_DAT_00017ad0 = *(short *)PTR_DAT_00017ad0 + 1;
  }
  return uVar3;
}

