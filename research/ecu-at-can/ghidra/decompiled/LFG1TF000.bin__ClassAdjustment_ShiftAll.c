/* Ghidra analysis output; verify against original SH instructions. */

/* SignedLOWWORDR4delta addedtoeachof3storedwords using36DFE/36E16; eachclamped+/-80;
   flagsunchanged.64directcases. */

void ClassAdjustment_ShiftAll(short param_1)

{
  int iVar1;
  int iVar2;
  
  iVar2 = 0;
  do {
    iVar1 = ClassAdjustment_ReadStored(iVar2);
    ClassAdjustment_SetClamped(iVar1 + param_1,iVar2);
    iVar2 = iVar2 + 1;
  } while (iVar2 < 3);
  return;
}

