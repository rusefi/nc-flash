/* Ghidra analysis output; verify against original SH instructions. */

/* Returns1 iff9564==2 OR9558==2, via original getters2DB4C/2D6D6. */

undefined4 Transition_CheckState9594Admission(void)

{
  char cVar1;
  char cVar2;
  undefined4 uVar3;
  
  cVar1 = (*(code *)PTR_Transition_ReadState9564_0002f110)();
  cVar2 = (*(code *)PTR_Transition_ReadState9558_0002f114)();
  uVar3 = 0;
  if ((cVar1 == '\x02') || (cVar2 == '\x02')) {
    uVar3 = 1;
  }
  return uVar3;
}

