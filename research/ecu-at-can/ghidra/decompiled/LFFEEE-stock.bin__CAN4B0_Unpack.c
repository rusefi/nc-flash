/* Ghidra analysis output; verify against original SH instructions. */

/* BE bytes4-5 ->6B08; bytes6-7 ->6B0A; executed with distinct payloads. */

void CAN4B0_Unpack(void)

{
  undefined *puVar1;
  
  puVar1 = PTR_CAN4B0_RxBuffer_00036010;
  *(ushort *)PTR_DAT_00036014 =
       (ushort)(byte)PTR_CAN4B0_RxBuffer_00036010[4] * 0x100 +
       (ushort)(byte)PTR_CAN4B0_RxBuffer_00036010[5];
  *(ushort *)PTR_DAT_00036018 = (ushort)(byte)puVar1[6] * 0x100 + (ushort)(byte)puVar1[7];
  return;
}

