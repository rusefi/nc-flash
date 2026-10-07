/* Ghidra analysis output; verify against original SH instructions. */

/* Complete original base3AC70, dynamic36A74, lower3676E and39C0A setter execute.
   Output=min15206,max(lower,s16(base)+dynamic+(s16(98DC)>>1)); lower
   stored9854.300full/100retained; base observed return not independent semantic model. */

void ClassAdjustment_ApplyToList(void)

{
  short sVar2;
  short sVar3;
  int iVar1;
  char *pcVar4;
  int iVar5;
  
  sVar2 = (*(code *)PTR_ClassApplication_BaseProducer_000367b4)();
  (*(code *)PTR_ClassAdjustment_InterpolatedConsumer_000367b8)();
  sVar3 = ClassAdjustment_ApplicationLowerLimit();
  iVar5 = (int)sVar3;
  iVar1 = (*(code *)PTR_FUN_000367c0)();
  iVar1 = ((int)*(short *)PTR_ClassAdjustment_UpdateInput_000367c4 >> 1) + iVar1 + (int)sVar2;
  if (iVar1 < iVar5) {
    iVar1 = iVar5;
  }
  if (*(short *)PTR_DAT_000367c8 < iVar1) {
    iVar1 = (int)*(short *)PTR_DAT_000367c8;
  }
  pcVar4 = (char *)(int)DAT_000367aa;
  *(short *)PTR_DAT_000367cc = (short)iVar5;
                    /* WARNING: Could not recover jumptable at 0x0003675e. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*(code *)PTR_ClassApplication_SetEntry_000367d0)((int)*pcVar4,iVar1);
  return;
}

