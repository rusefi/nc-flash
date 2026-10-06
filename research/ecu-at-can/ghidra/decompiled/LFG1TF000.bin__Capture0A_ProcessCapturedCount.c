/* Ghidra analysis output; verify against original SH instructions. */

/* Unsigned32 timestamp delta/10 ->88F8, calls20678; clears8900, saturating
   increments88F0/88F2/88F4.63 timestamp cases and both-capture shift lifecycles; physical
   wiring/clocks open. See tcu-reference-source.txt and earlier speed-fault.txt. */

undefined4 Capture0A_ProcessCapturedCount(int param_1)

{
  undefined *puVar1;
  uint uVar2;
  undefined4 uVar3;
  int iVar4;
  
  puVar1 = PTR_FUN_00017a28;
  iVar4 = *(int *)(int)DAT_00017a14;
  *(int *)(int)DAT_00017a14 = param_1;
  uVar2 = (*(code *)puVar1)(param_1,param_1 - iVar4);
  puVar1 = PTR_Reference_IngestCaptureAndFilter_00017a30;
  if (DAT_00017a2c < uVar2) {
    uVar2 = DAT_00017a2c;
  }
  *(uint *)PTR_DAT_00017a20 = uVar2;
  (*(code *)puVar1)();
  uVar3 = (*(code *)PTR_FUN_00017a38)(PTR_SpeedFault_OtherCaptureCount_00017a34);
  puVar1 = PTR_DAT_00017a3c;
  if ((undefined *)(uint)*(ushort *)PTR_DAT_00017a18 != PTR_DAT_00017a3c) {
    *(short *)PTR_DAT_00017a18 = *(short *)PTR_DAT_00017a18 + 1;
  }
  if ((undefined *)(uint)*(ushort *)PTR_SpeedFault_Capture0ACount_00017a1c != puVar1) {
    *(short *)PTR_SpeedFault_Capture0ACount_00017a1c =
         *(short *)PTR_SpeedFault_Capture0ACount_00017a1c + 1;
  }
  if ((undefined *)(uint)*(ushort *)PTR_DAT_00017a24 != puVar1) {
    *(short *)PTR_DAT_00017a24 = *(short *)PTR_DAT_00017a24 + 1;
  }
  return uVar3;
}

