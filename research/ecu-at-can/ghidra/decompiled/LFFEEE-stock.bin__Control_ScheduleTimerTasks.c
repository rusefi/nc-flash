/* Ghidra analysis output; verify against original SH instructions. */

/* 3584selection/countercases PASS:FA68/task7eachcall;51E0word++ oddbinarywheel11414
   firstsetbit;51E2byte++mod256 >=5 resets0/tailsFBE8.6899callbacks/1526upstreamrequests.
   Allcalleesexecute, noallnestedRAMoracle.
   Full600nativequeued150event1/120event2,298actualqueue3consumerRAMchecks; physicaltimingunproved.
   control-timer-event2.txt. */

uint Control_ScheduleTimerTasks(void)

{
  ushort uVar1;
  undefined *puVar2;
  undefined *puVar3;
  uint uVar4;
  uint uVar5;
  byte *pbVar6;
  
  puVar2 = PTR_PTR_000106b8;
  (**(code **)PTR_PTR_000106b8)(0);
  puVar3 = PTR_DAT_000106bc;
  *(short *)PTR_DAT_000106bc = *(short *)PTR_DAT_000106bc + 1;
  uVar1 = *(ushort *)puVar3;
  uVar5 = (uint)(short)uVar1;
  uVar4 = (uint)uVar1;
  if ((uVar1 & 1) != 0) {
    for (pbVar6 = PTR_DAT_000106c0; pbVar6 < PTR_DAT_000106c0 + 9; pbVar6 = pbVar6 + 1) {
      uVar5 = (uVar5 & 0xffff) >> 1;
      if ((uVar5 & 1) != 0) {
        uVar4 = (**(code **)(puVar2 + (uint)*pbVar6 * 4))(0);
        break;
      }
      uVar4 = uVar5;
    }
  }
  puVar3 = PTR_DAT_000106c4;
  *PTR_DAT_000106c4 = *PTR_DAT_000106c4 + '\x01';
  if ((byte)*puVar3 < 5) {
    return uVar4;
  }
  *puVar3 = 0;
  uVar5 = (**(code **)(puVar2 + 0x34))(0);
  return uVar5;
}

