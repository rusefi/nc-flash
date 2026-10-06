/* Ghidra analysis output; verify against original SH instructions. */

/* Returns1 iff2DB4C reads9564==2. */

bool Transition_CheckState959CAdmission(void)

{
  char cVar1;
  
  cVar1 = (*(code *)PTR_Transition_ReadState9564_0002f510)();
  return cVar1 == '\x02';
}

