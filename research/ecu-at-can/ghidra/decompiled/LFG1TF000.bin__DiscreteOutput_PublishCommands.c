/* Ghidra analysis output; verify against original SH instructions. */

/* SelectsA5CAoverride iffA5CF==1 elseA5C5;84A0 exact1/4 forces0; publishesrawbyte to8A1C/A5C0.
   CompleteRAMandtaskboundaryverified. See tcu-source-inhibit.txt. */

void DiscreteOutput_PublishCommands(void)

{
  char cVar1;
  char cVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  int iVar6;
  
  iVar6 = 0;
  cVar1 = *PTR_Startup_AdcAReadinessState_00052e44;
  iVar3 = (int)DAT_00052e3a;
  iVar4 = (int)DAT_00052e40;
  do {
    cVar2 = *(char *)(iVar4 + iVar6);
    if (*(char *)(iVar3 + iVar6) == '\x01') {
      cVar2 = *(char *)(iVar6 + DAT_00052e3c);
    }
    iVar5 = (int)cVar2;
    if ((cVar1 == '\x01') || (cVar1 == '\x04')) {
      iVar5 = 0;
    }
    (*(code *)PTR_DiscreteOutput_StorePublishedCommand_00052e48)(iVar6,iVar5);
    *(char *)(iVar6 + DAT_00052e3e) = (char)iVar5;
    iVar6 = iVar6 + 1;
  } while (iVar6 < 5);
  return;
}

