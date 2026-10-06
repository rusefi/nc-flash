/* Ghidra analysis output; verify against original SH instructions. */

/* STATIC:84F5==1 initializes2/phase7;==2 calls1E5F6(84F4&7); always increments84F4. Full task
   timing remains open. */

uint Task_DispatchApplicationPhase(void)

{
  undefined *puVar1;
  uint uVar2;
  
  puVar1 = PTR_DAT_00012764;
  uVar2 = (uint)*(byte *)(int)DAT_00012762;
  if (uVar2 != 0) {
    if (uVar2 == 1) {
      *(byte *)(int)DAT_00012762 = 2;
      *puVar1 = 7;
    }
    else if (uVar2 == 2) {
      uVar2 = (*(code *)PTR_Task_ApplicationPeriodicBody_00012794)(*PTR_DAT_00012764 & 7);
    }
  }
  *puVar1 = *puVar1 + '\x01';
  return uVar2;
}

