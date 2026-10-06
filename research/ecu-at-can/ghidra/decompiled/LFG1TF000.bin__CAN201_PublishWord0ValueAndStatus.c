/* Ghidra analysis output; verify against original SH instructions. */

/* 80E8*100/256 ->809E;A4E4=4 when92C9bit6,else1 when8816==2,else2. Invalid raw holds numeric
   separately from substitution. */

uint CAN201_PublishWord0ValueAndStatus(void)

{
  char cVar1;
  byte bVar2;
  
  CAN201_Word0Rescaled = (*(code *)PTR_FUN_00050cec)();
  cVar1 = *PTR_ApplicationFaultFlags92C9_00050cf0;
  if (((int)cVar1 & 0x40U) != 0) {
    *PTR_CAN201_Word0ApplicationStatus_00050ce8 = 4;
    return (int)cVar1;
  }
  bVar2 = *PTR_DAT_00050cf4;
  if (bVar2 == 2) {
    *PTR_CAN201_Word0ApplicationStatus_00050ce8 = 1;
    return 1;
  }
  *PTR_CAN201_Word0ApplicationStatus_00050ce8 = 2;
  return (uint)bVar2;
}

