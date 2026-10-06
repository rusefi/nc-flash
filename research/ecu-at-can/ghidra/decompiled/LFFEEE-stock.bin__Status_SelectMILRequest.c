/* Ghidra analysis output; verify against original SH instructions. */

/* Input1 iff91BD==0 and(protected24EE==1 or6536==0);8B8A0 diagnostic override then91BE.192
   display/override/packing cases verified. */

void Status_SelectMILRequest(void)

{
  char cVar1;
  undefined1 uVar2;
  undefined4 uVar3;
  
  cVar1 = (*(code *)PTR_Protected_ReadByteOrDefault_000777d0)(PTR_DAT_000777cc,0);
  if ((*PTR_DAT_000777c0 == '\0') && ((cVar1 == '\x01' || (*PTR_DAT_000777b8 == '\0')))) {
    uVar3 = 1;
  }
  else {
    uVar3 = 0;
  }
  uVar2 = (*(code *)PTR_Status_OverrideMILRequest_000777d4)(uVar3);
  *PTR_DAT_000777d8 = uVar2;
  return;
}

