/* Ghidra analysis output; verify against original SH instructions. */

/* Record-state/child/timing gates control assertion and release;2268 cases plus6 release
   boundaries. Accepted active cancellation calls96F4 and2F2A0. See output-inhibition.txt. */

void Output_ApplyChangedInhibitMask(undefined4 param_1,ushort param_2)

{
  bool bVar1;
  undefined *puVar2;
  undefined *puVar3;
  int iVar4;
  char cVar5;
  char *pcVar6;
  byte *pbVar7;
  ushort uVar9;
  char *pcVar8;
  char *pcVar10;
  
  puVar3 = PTR_Output_TimerSoftwareRecords_000202c8;
  puVar2 = PTR_Output_CancelTimerChannel_000202c0;
  pcVar6 = PTR_Output_CylinderRecords_000202c4 + DAT_000202ba;
  pcVar10 = PTR_Output_CylinderRecords_000202c4;
  do {
    if (pcVar6 <= pcVar10) {
      return;
    }
    uVar9 = param_2 & *(ushort *)
                       (PTR_Output_CylinderMaskBits_000203ec + (uint)(byte)pcVar10[0xc] * 2);
    if ((((pcVar10[1] == '\x01') && (uVar9 == 0)) || ((pcVar10[1] == '\0' && (uVar9 != 0)))) &&
       (iVar4 = Output_ForwardPositionDistance(param_1,*(undefined4 *)(pcVar10 + 8)), -1 < iVar4)) {
      if (uVar9 == 0) {
        if (pcVar10[2] == '\x01') {
LAB_000203be:
          pcVar10[1] = '\0';
        }
        else if (pcVar10[2] == '\0') {
          cVar5 = (**(code **)(PTR_Output_SchedulerModes_000203f0 + *pcVar10 * 0x10 + 0xc))(pcVar10)
          ;
          if (cVar5 == '\x01') goto LAB_000203be;
          pcVar10[2] = '\x02';
        }
      }
      else if (pcVar10[2] == '\x01') {
        bVar1 = true;
        for (pbVar7 = (byte *)(pcVar10 + 0x10); pbVar7 < pcVar10 + 0x28; pbVar7 = pbVar7 + 0x18) {
          if (pbVar7[1] == 1) {
            if (puVar3[(uint)*pbVar7 * 0x18 + 0x13] == '\0') {
LAB_0002035e:
              bVar1 = false;
              break;
            }
          }
          else if (pbVar7[1] == 2) goto LAB_0002035e;
        }
        if (bVar1) {
          for (pcVar8 = pcVar10 + 0x10; pcVar8 < pcVar10 + 0x28; pcVar8 = pcVar8 + 0x18) {
            (*(code *)puVar2)((int)*pcVar8);
            (*(code *)PTR_Output_ClearPendingDuration_000203f4)((int)*pcVar8);
          }
          pcVar10[2] = '\0';
          pcVar10[1] = '\x01';
        }
      }
      else if (pcVar10[2] == '\0') {
        pcVar10[1] = '\x01';
      }
    }
    pcVar10 = pcVar10 + 0x28;
  } while( true );
}

