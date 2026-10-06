/* Ghidra analysis output; verify against original SH instructions. */

/* Executed event counters: neutral10 decrements on qualifying clutch transitions; clutch8 on
   held-activity falling edges. Transition latches/reset reload. */

char LocalInputDiag_UpdateEventCounters(void)

{
  char cVar1;
  undefined *puVar2;
  char cVar3;
  char cVar4;
  char cVar5;
  
  cVar5 = *PTR_DAT_0006c050;
  cVar3 = (*(code *)PTR_FUN_0006c028)(PTR_DAT_0006c024);
  cVar4 = (*(code *)PTR_FUN_0006c028)(PTR_DAT_0006c054);
  puVar2 = PTR_DAT_0006c058;
  cVar1 = *PTR_DAT_0006c048;
  if (cVar3 == '\x01') {
    *PTR_DAT_0006c058 = 0;
  }
  else if (cVar5 != cVar4) {
    *PTR_DAT_0006c058 = 1;
  }
  if ((*PTR_DAT_0006c02c == '\x01') || (cVar3 == '\x01')) {
    *PTR_LocalInputDiag_NeutralEventCounter_0006c018 = *PTR_DAT_0006c014;
  }
  else if ((*PTR_DAT_0006c140 == '\x01') &&
          ((cVar4 != cVar5 && (*PTR_LocalInputDiag_NeutralEventCounter_0006c018 != '\0')))) {
    *PTR_LocalInputDiag_NeutralEventCounter_0006c018 =
         *PTR_LocalInputDiag_NeutralEventCounter_0006c018 + (char)DAT_0006c13c;
  }
  if ((*puVar2 == '\x01') || (cVar3 == '\x01')) {
    *PTR_LocalInputDiag_ClutchEventCounter_0006c144 = *PTR_DAT_0006c148;
    cVar5 = '\x01';
  }
  else {
    cVar5 = cVar1;
    if ((cVar1 == '\0') &&
       ((cVar5 = *PTR_DAT_0006c14c, cVar5 == '\x01' &&
        (*PTR_LocalInputDiag_ClutchEventCounter_0006c144 != '\0')))) {
      *PTR_LocalInputDiag_ClutchEventCounter_0006c144 =
           *PTR_LocalInputDiag_ClutchEventCounter_0006c144 + (char)DAT_0006c13c;
    }
  }
  *PTR_DAT_0006c14c = cVar1;
  return cVar5;
}

