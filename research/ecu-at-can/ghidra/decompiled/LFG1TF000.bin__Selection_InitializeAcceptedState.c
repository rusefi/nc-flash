/* Ghidra analysis output; verify against original SH instructions. */

/* Loadsindex13/606F, copies8081/8085/9C85/9C86/9C80;9C87=FF,9C88/89=0. Executed before144
   transitionfixtures. */

void Selection_InitializeAcceptedState(void)

{
  undefined1 *puVar1;
  byte *pbVar2;
  
  CAN231_SixStateSource = (*(code *)PTR_StateCache_ReadByte_00048c00)(0x13);
  pbVar2 = (byte *)(int)DAT_00048bf4;
  *(byte *)(int)DAT_00048bf2 = CAN231_SixStateSource;
  *pbVar2 = CAN231_SixStateSource;
  puVar1 = (undefined1 *)(int)DAT_00048bfa;
  Selection_NextIndex = CAN231_SixStateSource;
  *(char *)(int)DAT_00048bf8 = (char)DAT_00048bf6;
  *puVar1 = 0;
  *(undefined1 *)(int)DAT_00048bfc = 0;
  *PTR_DAT_00048c04 = CAN231_SixStateSource;
  return;
}

