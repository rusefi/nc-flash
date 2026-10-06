/* Ghidra analysis output; verify against original SH instructions. */

/* Event/state table5D3E4. Event3 receives payload[u16 group,u8 phaseindex] and calls31C18 only in
   state2. Original group acknowledgements and idle duplicate handling verified; see
   tcu-phase-retirement.txt. */

void Phase_DispatchEvent(ushort param_1,short *param_2)

{
  char cVar1;
  int iVar2;
  
  iVar2 = -1;
  if (param_1 == 0) {
    iVar2 = Phase_InitializeDispatcher();
  }
  else {
    cVar1 = PTR_Phase_EventStateTable_00031700[(int)Phase_DispatchState + (uint)param_1 * 3];
    if (cVar1 == '\x01') {
      iVar2 = Phase_CreateAndNotifyGroups((int)*param_2,(int)param_2[1],(int)param_2[2]);
    }
    else if (cVar1 == '\x02') {
      iVar2 = Phase_ServiceRecords();
    }
    else if (cVar1 == '\x03') {
      iVar2 = Phase_AcknowledgeAndRetire((int)*(char *)(param_2 + 1),(int)*param_2);
    }
    else if (cVar1 == '\x04') {
      iVar2 = Request_ServicePeriodicGroups();
    }
  }
  if (iVar2 != -1) {
    Phase_DispatchState = (char)iVar2;
  }
  return;
}

