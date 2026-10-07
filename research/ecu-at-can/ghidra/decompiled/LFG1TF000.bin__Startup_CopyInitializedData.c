/* Ghidra analysis output; verify against original SH instructions. */

/* Executed all992 bytes5F220..5F5FF ->FFFFAD4C..FFFFB12B; supplies stock list descriptorsB028/B02C
   andAD4E=0 for137B4 stored array initialization. Three sentinel copies checked in
   tcu-stored-adjustments.txt; full boot hardware not simulated. */

undefined4 Startup_CopyInitializedData(void)

{
  undefined *puVar1;
  undefined4 uVar2;
  undefined4 *puVar3;
  undefined4 *puVar4;
  
  puVar1 = PTR_DAT_00015d24;
  puVar3 = DAT_00015d1c;
  puVar4 = (undefined4 *)PTR_DAT_00015d20;
  do {
    uVar2 = *puVar3;
    *puVar4 = uVar2;
    puVar3 = puVar3 + 1;
    puVar4 = puVar4 + 1;
  } while (puVar3 < puVar1);
  return uVar2;
}

