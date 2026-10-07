/* Ghidra analysis output; verify against original SH instructions. */

/* Executed84F5==1 setsstage2/phase7 thenincrementsphase8;==2 invokes1E5F6(84F4&7);
   otherstagesonlyincrementbyte84F4. Fulltaskreturns/phasewrap verified; physicalcadence open. See
   tcu-application-order.txt. */

uint Task_DispatchApplicationPhase(void)

{
  undefined *puVar1;
  uint uVar2;
  
  puVar1 = PTR_Task_ApplicationPhaseCounter_00012764;
  uVar2 = (uint)*(byte *)(int)DAT_00012762;
  if (uVar2 != 0) {
    if (uVar2 == 1) {
      *(byte *)(int)DAT_00012762 = 2;
      *puVar1 = 7;
    }
    else if (uVar2 == 2) {
      uVar2 = (*(code *)PTR_Task_ApplicationPeriodicBody_00012794)
                        (*PTR_Task_ApplicationPhaseCounter_00012764 & 7);
    }
  }
  *puVar1 = *puVar1 + '\x01';
  return uVar2;
}

