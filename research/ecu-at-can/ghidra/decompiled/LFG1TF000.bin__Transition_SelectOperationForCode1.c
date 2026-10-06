/* Ghidra analysis output; verify against original SH instructions. */

/* 3159A(1) signedphase>=1 returns9, otherwise8. Calledby4740C previouscode1,next1 in bounded
   originalcreation; othercontexts open. */

undefined4 Transition_SelectOperationForCode1(void)

{
  char cVar1;
  undefined4 uVar2;
  
  uVar2 = 8;
  cVar1 = (*(code *)PTR_ApplicationPhase_ReadForCode_000477fc)(1);
  if ('\0' < cVar1) {
    uVar2 = 9;
  }
  return uVar2;
}

