/* Ghidra analysis output; verify against original SH instructions. */

/* Lowbyte selects stock timer writes based on TCNT1A+4; DCNT8F/G/H duplicate writes through11070
   and GR1F/G/H offsets. Exact writes verified including16bit wrap; clock/pin effects unmodeled. */

void Acquisition_ConfigureAlternateTimers(char param_1)

{
  undefined *puVar1;
  int iVar2;
  short sVar3;
  int iVar4;
  short sVar5;
  short sVar6;
  undefined4 local_24 [2];
  
  sVar3 = *(short *)PTR_DAT_00005dd0;
  iVar2 = (int)sVar3;
  if (param_1 == '\0') {
    iVar4 = iVar2;
    iVar2 = (int)*(short *)PTR_DAT_00005dd4;
    sVar5 = sVar3;
    sVar3 = 0;
  }
  else {
    sVar5 = 0;
    iVar4 = (int)*(short *)PTR_DAT_00005e80;
  }
  (*(code *)PTR_FUN_00005e84)(local_24,(int)DAT_00005e6c);
  puVar1 = PTR_Output_WriteCounterTwice_00005e88;
  sVar6 = *(short *)(int)DAT_00005e6e + 4;
  (*(code *)PTR_Output_WriteCounterTwice_00005e88)((int)DAT_00005e70,iVar2);
  *(short *)(int)DAT_00005e72 = sVar5 + sVar6;
  (*(code *)puVar1)((int)DAT_00005e74,iVar4);
  *(short *)(int)DAT_00005e76 = sVar3 + sVar6;
  (*(code *)puVar1)((int)DAT_00005e78,1);
  *(short *)(int)DAT_00005e7a = sVar6 + *(short *)PTR_DAT_00005e8c;
  (*(code *)PTR_FUN_00005e90)(local_24[0]);
  *PTR_DAT_00005e94 = 0;
  return;
}

