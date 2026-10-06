/* Ghidra analysis output; verify against original SH instructions. */

/* BE words bytes 0-1,2-3,5-6 and bytes 4,7. Paired code verified. */

void CAN216_Unpack(void)

{
  undefined *puVar1;
  undefined *puVar2;
  
  puVar1 = PTR_CAN216_RxBuffer_000350c8;
  *(ushort *)PTR_DAT_000350cc =
       (ushort)(byte)*PTR_CAN216_RxBuffer_000350c8 * 0x100 +
       (ushort)(byte)PTR_CAN216_RxBuffer_000350c8[1];
  puVar2 = PTR_DAT_000350d4;
  *(ushort *)PTR_DAT_000350d0 = (ushort)(byte)puVar1[2] * 0x100 + (ushort)(byte)puVar1[3];
  *puVar2 = puVar1[4];
  *(ushort *)PTR_DAT_000350d8 = (ushort)(byte)puVar1[5] * 0x100 + (ushort)(byte)puVar1[6];
  *PTR_DAT_000350dc = puVar1[7];
  return;
}

