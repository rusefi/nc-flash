/* Ghidra analysis output; verify against original SH instructions. */

/* 6B8C combines91BD==1 bit15,91BE==1 bit14,693A==1 bit6. Packing370A6..370DC maps these to byte5
   bits7/6 and byte6 bit6. */

char CAN420_BuildWarningWord(void)

{
  char cVar1;
  ushort uVar2;
  
  uVar2 = 0;
  if (*PTR_DAT_00037268 == '\x01') {
    uVar2 = (ushort)PTR_LAB_0003726c;
  }
  if (*PTR_DAT_00037270 == '\x01') {
    uVar2 = uVar2 | DAT_0003723e;
  }
  cVar1 = *PTR_DAT_00037274;
  if (cVar1 == '\x01') {
    uVar2 = uVar2 | 0x40;
  }
  *(ushort *)PTR_DAT_00037278 = uVar2;
  return cVar1;
}

