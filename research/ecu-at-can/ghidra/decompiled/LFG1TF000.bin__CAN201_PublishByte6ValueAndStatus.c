/* Ghidra analysis output; verify against original SH instructions. */

/* A4D4=floor(8098*10/256);A4D6=4 if92D5mask08 else1 if880A==2 else2.1536 raw/held/fault cases. */

uint CAN201_PublishByte6ValueAndStatus(void)

{
  char cVar1;
  byte bVar2;
  undefined2 uVar3;
  
  uVar3 = (*(code *)PTR_FUN_00050aac)();
  *(undefined2 *)PTR_CAN201_Byte6PublishedValue_00050aa4 = uVar3;
  cVar1 = *PTR_ApplicationFaultFlags92D5_00050ab0;
  if (((int)cVar1 & 8U) != 0) {
    *PTR_CAN201_Byte6PublishedStatus_00050aa8 = 4;
    return (int)cVar1;
  }
  bVar2 = *PTR_CAN201_Byte6Validity_00050ab4;
  if (bVar2 == 2) {
    *PTR_CAN201_Byte6PublishedStatus_00050aa8 = 1;
    return 1;
  }
  *PTR_CAN201_Byte6PublishedStatus_00050aa8 = 2;
  return (uint)bVar2;
}

