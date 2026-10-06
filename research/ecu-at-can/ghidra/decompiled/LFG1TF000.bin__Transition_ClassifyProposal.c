/* Ghidra analysis output; verify against original SH instructions. */

/* Produces9C52/54, adjusts history via475DC, looks up47670; operation20->11,21/22->10,25->9,26->3
   decimal. Always stores9C50.1024 direct wrapper cases plus fullcaller observation;
   tcu-transition-classification.txt. */

undefined4 Transition_ClassifyProposal(char param_1,char param_2)

{
  char cVar1;
  int iVar2;
  undefined4 uVar3;
  undefined4 uVar4;
  
  iVar2 = (int)(char)CAN231_SixStateSource;
  cVar1 = *PTR_Transition_ReferenceHistory_000474c0;
  Transition_UpdateQualificationFlags();
  uVar3 = Transition_AdjustReferenceHistory((int)cVar1,iVar2);
  uVar4 = Transition_LookupQualifiedCode(uVar3,iVar2,(int)param_2);
  if (param_1 == '\x14') {
    uVar4 = 0xb;
  }
  else if ((param_1 == '\x15') || (param_1 == '\x16')) {
    uVar4 = 10;
  }
  else if (param_1 == '\x19') {
    uVar4 = 9;
  }
  else if (param_1 == '\x1a') {
    uVar4 = 3;
  }
  *PTR_Transition_ReferenceHistory_000474c0 = (char)uVar3;
  return uVar4;
}

