/* Ghidra analysis output; verify against original SH instructions. */

/* Kind0 creates all ten groups. Kind3 phase completion notifies metadata0 groups only, skips
   already acknowledged entries; original callbacks/event3 retire records in full initialization
   fixtures. See tcu-phase-retirement.txt. */

uint Phase_NotifyRequestGroups(char param_1,byte param_2)

{
  int iVar1;
  undefined *puVar2;
  undefined *puVar3;
  uint uVar4;
  byte *pbVar5;
  int iVar6;
  int iVar7;
  int iStack_2c;
  uint uStack_24;
  
  uVar4 = (uint)param_1;
  if (uVar4 == 0) {
    uStack_24 = 1;
    iStack_2c = 1;
  }
  else {
    uStack_24 = (uint)(uVar4 == 1);
    iStack_2c = 3;
  }
  iVar7 = 0;
  iVar1 = (uint)param_2 * 0xf;
  do {
    puVar3 = PTR_Phase_RecordRing_000320c0;
    puVar2 = PTR_Request_PeriodicGroupRecords_000320b8;
    if (9 < iVar7) {
      return uVar4;
    }
    iVar6 = iVar7 * 4;
    if ((PTR_Request_PeriodicGroupRecords_000320b8[iVar6 + 2] == '\0') ||
       (uVar4 = (uint)(char)PTR_Request_PeriodicGroupRecords_000320b8[iVar6 + 2], uVar4 == uStack_24
       )) {
      if (iStack_2c == 1) {
        pbVar5 = (byte *)(*(code *)PTR_EventMessage_NextBuffer_000320bc)();
        *pbVar5 = param_2;
        pbVar5[1] = puVar3[iVar1 + 10];
        pbVar5[2] = puVar3[iVar1 + 0xb];
        pbVar5[3] = puVar3[iVar1 + 0xc];
        uVar4 = (uint)*(ushort *)(puVar2 + iVar6) << 0x10 | 1;
      }
      else {
        uVar4 = 1;
        if (PTR_Phase_RecordRing_000320c0[iVar7 + iVar1] == '\x01') goto LAB_00032052;
        pbVar5 = (byte *)(*(code *)PTR_EventMessage_NextBuffer_000320bc)();
        *pbVar5 = param_2;
        uVar4 = (uint)*(ushort *)(puVar2 + iVar6) << 0x10 | 3;
      }
      (*(code *)PTR_EventQueue_Enqueue_000320c4)(0,1,uVar4);
      uVar4 = (*(code *)PTR_EventQueue_Drain_000320c8)(0);
    }
LAB_00032052:
    iVar7 = iVar7 + 1;
  } while( true );
}

