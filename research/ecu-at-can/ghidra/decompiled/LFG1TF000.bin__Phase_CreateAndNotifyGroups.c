/* Ghidra analysis output; verify against original SH instructions. */

/* Event1 append, eight5D3F4callbacks,321A6 and31F64(kind0). Prior144resetcases/12coupledlifecycles.
   Natural48F20 event1 nowexecutesinside complete126EC after62initializers;
   multiplephase/managedrecords andrealacks/retirement observed/modelchecked.
   tcu-initialized-requests.txt. */

undefined4 Phase_CreateAndNotifyGroups(undefined4 param_1,undefined4 param_2,undefined4 param_3)

{
  undefined *puVar1;
  code *pcVar2;
  byte bVar3;
  undefined4 *puVar4;
  undefined4 *puVar5;
  undefined4 local_24;
  
  puVar1 = PTR_Phase_RecordRing_00031a6c;
  local_24 = 0xffffffff;
  if ((byte)PTR_Phase_RecordRing_00031a6c[DAT_00031a4e] < 0x10) {
    bVar3 = PTR_Phase_RecordRing_00031a6c[DAT_00031a50] +
            PTR_Phase_RecordRing_00031a6c[DAT_00031a4e] + 0x10 & 0xf;
    Phase_AppendRecord(param_1,param_2,param_3);
    DAT_ffff8089 = (undefined1)param_1;
    DAT_ffff808a = (undefined1)param_2;
    puVar4 = (undefined4 *)(PTR_Phase_CreationCallbacks_00031a70 + 0x20);
    puVar5 = (undefined4 *)PTR_Phase_CreationCallbacks_00031a70;
    do {
      pcVar2 = (code *)*puVar5;
      puVar5 = puVar5 + 1;
      (*pcVar2)(param_1,param_2,param_3);
    } while (puVar5 < puVar4);
    (*(code *)PTR_FUN_00031a74)(bVar3);
    Phase_NotifyRequestGroups(0,bVar3);
    if (puVar1[DAT_00031a4e] != '\0') {
      local_24 = 2;
    }
  }
  return local_24;
}

