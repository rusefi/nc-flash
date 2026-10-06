/* Ghidra analysis output; verify against original SH instructions. */

/* Writes protected24EE=(protected24EC OR6E53) AND protected9462!=1.32 receiver/gate cases;7774A
   forwards to91BE and CAN420 byte5 bit6 subject to display/diagnostic gates. */

void Status_CombineLocalAndATReport(void)

{
  char cVar1;
  undefined4 uVar2;
  
  cVar1 = (*(code *)PTR_Protected_ReadByteOrDefault_0007769c)(PTR_DAT_00077694,0);
  if (((cVar1 == '\0') && (*PTR_DAT_000776a0 == '\0')) ||
     (cVar1 = (*(code *)PTR_FUN_00077690)(PTR_DAT_0007768c), cVar1 == '\x01')) {
    uVar2 = 0;
  }
  else {
    uVar2 = 1;
  }
  (*(code *)PTR_FUN_00077698)(PTR_DAT_000776a4,uVar2);
  return;
}

