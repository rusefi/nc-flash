/* Ghidra analysis output; verify against original SH instructions. */

/* Unsigned88F8 capped57344; special8080zero/80E8>=7680/bit2 early return. Otherwise
   historysum<=91643 and ratio outside128..538 replaces one outlier with prior period, bit3
   remembers replacement.320 cases; updates18-entry ring and3-count91AA,clears810D/91AC. See
   tcu-reference-source.txt. */

undefined4 Reference_IngestCaptureAndFilter(void)

{
  undefined *puVar1;
  uint uVar2;
  uint uVar3;
  undefined4 uVar4;
  byte *pbVar5;
  uint uVar6;
  byte *pbVar7;
  uint uVar8;
  byte bVar9;
  
  *PTR_DAT_00020744 = *PTR_DAT_0002073c;
  bVar9 = *(byte *)(int)DAT_00020736;
  if (((TransmissionStateClass == 0) && (*(short *)PTR_DAT_00020750 <= CAN201_Word0ApplicationValue)
      ) && ((*(byte *)(int)DAT_00020738 & 4) != 0)) {
    return 1;
  }
  uVar8 = *(uint *)PTR_DAT_00020754;
  uVar2 = Reference_ReadResetPeriod();
  if (uVar2 < uVar8) {
    uVar8 = uVar2;
  }
  uVar2 = Reference_SumCaptureHistory((int)DAT_0002073a);
  pbVar7 = (byte *)(int)DAT_00020738;
  if (((*pbVar7 & 2) != 0) && (uVar2 <= *(uint *)PTR_DAT_00020758)) {
    *pbVar7 = *pbVar7 & 0xfd;
  }
  uVar6 = *(uint *)(PTR_Reference_CaptureHistory_0002075c + (uint)bVar9 * 4);
  uVar3 = (*(code *)PTR_FUN_00020760)(uVar8 << 8,uVar6);
  if (((*(uint *)PTR_DAT_00020764 < uVar2) ||
      ((uVar3 <= *(ushort *)PTR_DAT_00020768 && (*(ushort *)PTR_DAT_0002076c <= uVar3)))) ||
     ((*(byte *)(int)DAT_00020738 & 8) != 0)) {
    *pbVar7 = *pbVar7 & 0xf7;
  }
  else {
    *pbVar7 = *pbVar7 | 8;
    uVar8 = uVar6;
  }
  bVar9 = bVar9 + 1;
  if ((byte)*PTR_DAT_00020848 <= bVar9) {
    bVar9 = 0;
  }
  pbVar7 = (byte *)(int)DAT_00020840;
  pbVar5 = (byte *)(int)DAT_00020842;
  *(uint *)(PTR_Reference_CaptureHistory_0002084c + (uint)bVar9 * 4) = uVar8;
  *pbVar7 = bVar9;
  puVar1 = PTR_DAT_00020850;
  *pbVar5 = *pbVar5 + 1;
  if ((byte)*puVar1 <= *pbVar5) {
    *pbVar5 = 0;
  }
  puVar1 = PTR_FUN_00020858;
  *PTR_DAT_00020854 = 0;
  uVar4 = (*(code *)puVar1)();
  puVar1 = PTR_FUN_0002085c;
  *(undefined2 *)(int)DAT_00020844 = 0;
  (*(code *)puVar1)(uVar4);
  (*(code *)PTR_FUN_00020860)();
                    /* WARNING: Could not recover jumptable at 0x000207cc. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  uVar4 = (*(code *)PTR_LAB_00020864)();
  return uVar4;
}

