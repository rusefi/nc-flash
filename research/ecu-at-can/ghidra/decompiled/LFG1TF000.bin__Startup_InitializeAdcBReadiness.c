/* Ghidra analysis output; verify against original SH instructions. */

/* 256 wholeRAM cases PASS:84D8=1,84DAword0,84E0/84E4long0; otherRAM preserved.
   Originalinitializedchains reachstate3 through11DEE withoutforcingreadyflag. tcu-readiness-b.txt.
    */

void Startup_InitializeAdcBReadiness(void)

{
  undefined4 *puVar1;
  undefined4 *puVar2;
  
  puVar1 = (undefined4 *)(int)DAT_00011ebc;
  *PTR_Startup_AdcBReadinessState_00011ec8 = 1;
  puVar2 = (undefined4 *)(int)DAT_00011ebe;
  *(undefined2 *)(int)DAT_00011eba = 0;
  *puVar1 = 0;
  *puVar2 = 0;
  return;
}

