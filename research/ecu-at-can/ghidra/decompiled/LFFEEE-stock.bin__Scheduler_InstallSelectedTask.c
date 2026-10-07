/* Ghidra analysis output; verify against original SH instructions. */

/* 64newtaskcases plus512originalsavedstate12dispatches
   PASS:wholeRAM/hook/temporarycallerstack/allrestoredregisters. 36F0/E7D4/38B4
   publishes45CC;423C+12-stocktype4 selects3EB4/3F00. Actualtask4->task7->task4
   preemption600outercycles PASS; explicitarrival/frame. control-preemption.txt. */

void Scheduler_InstallSelectedTask(int param_1,short param_2)

{
  undefined *puVar1;
  undefined4 uVar2;
  byte *pbVar3;
  char *pcVar4;
  
  puVar1 = PTR_PTR_00003d68;
  pbVar3 = PTR_DAT_00003d64 + param_2 * 0x10;
  pcVar4 = *(char **)(pbVar3 + 4);
  *(short *)(param_1 + 4) = param_2;
  *(byte **)(param_1 + 0x18) = pbVar3;
  *(char **)(param_1 + 0x14) = pcVar4;
  if (*(int *)puVar1 != 0) {
    (*(code *)PTR_FUN_00003d6c)();
  }
  *(undefined4 *)(param_1 + 8) = 0;
  if (*pcVar4 == 0) {
    pcVar4[1] = pbVar3[2];
    uVar2 = *(undefined4 *)(param_1 + 0xc);
    *(undefined4 *)(pcVar4 + 4) = uVar2;
    (*(code *)PTR_Scheduler_EnterTaskFromStackFrame_00003d70)(*(undefined4 *)(pbVar3 + 8),uVar2);
    return;
  }
                    /* WARNING: Could not recover jumptable at 0x00003d60. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (**(code **)(PTR_LAB_00003d74 + ((int)*pcVar4 - (uint)*pbVar3)))(*(undefined4 *)(param_1 + 0xc));
  return;
}

