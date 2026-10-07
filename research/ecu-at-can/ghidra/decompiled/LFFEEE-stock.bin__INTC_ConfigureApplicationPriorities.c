/* Ghidra analysis output; verify against original SH instructions. */

/* 256originalAA4A/AA94cases PASS:13orderedwordwritesED00..ED18;IPRJED12=0999
   givescompatibleCMTI1priority9,ED18ICR=00FF. WholeRAM/savedregisters/SR unchanged.
   NoICRpin/priorityarbitration/physicaladmission model. RetainedIRQfixtureSRF0 isexplicit.
   control-interrupt-timer.txt. */

void INTC_ConfigureApplicationPriorities(void)

{
  undefined2 *puVar1;
  undefined2 *puVar2;
  undefined2 *puVar3;
  undefined2 uVar4;
  undefined2 uVar5;
  
  uVar5 = DAT_0000aae4;
  puVar3 = (undefined2 *)(int)DAT_0000aae6;
  *puVar3 = DAT_0000aae4;
  *(short *)(int)DAT_0000aae8 = (short)PTR_LAB_0000ab04;
  *(short *)(int)DAT_0000aaea = (short)DAT_0000ab08;
  uVar4 = (undefined2)DAT_0000ab0c;
  puVar3[3] = uVar4;
  puVar1 = (undefined2 *)(int)DAT_0000aaee;
  *puVar1 = DAT_0000aaec;
  *(short *)(int)DAT_0000aaf0 = (short)DAT_0000ab10;
  puVar3[6] = uVar4;
  puVar1[3] = (short)PTR_LAB_00009998_1_0000ab14;
  puVar2 = (undefined2 *)(int)DAT_0000aaf2;
  *puVar2 = (short)PTR_LAB_0000ab18;
  puVar3[9] = uVar5;
  uVar5 = SUB42(PTR_LAB_00009908_1_0000ab1c,0);
  *(undefined2 *)(int)DAT_0000aaf4 = uVar5;
  puVar2[3] = uVar5;
  puVar1[8] = DAT_0000aaf6;
  return;
}

