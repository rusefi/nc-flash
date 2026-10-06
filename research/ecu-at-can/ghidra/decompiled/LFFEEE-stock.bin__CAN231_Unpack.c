/* Ghidra analysis output; verify against original SH instructions. */

/* Reads only byte0, byte1 and BE word at bytes2-3. */

void CAN231_Unpack(void)

{
  undefined *puVar1;
  
  puVar1 = PTR_CAN231_RxBuffer_00035c04;
  *PTR_DAT_00035c08 = *PTR_CAN231_RxBuffer_00035c04;
  *PTR_DAT_00035c0c = puVar1[1];
  *(ushort *)PTR_DAT_00035c10 = (ushort)(byte)puVar1[2] * 0x100 + (ushort)(byte)puVar1[3];
  return;
}

