/* Ghidra analysis output; verify against original SH instructions. */

/* Executed BE bytes0..1 ->6AB6, bytes2..3 ->6AB8. Sender and physical units unknown. */

void CAN21A_Unpack(void)

{
  undefined *puVar1;
  
  puVar1 = PTR_CAN21A_RxBuffer_00035774;
  *(ushort *)PTR_CAN21A_RawWord0_00035778 =
       (ushort)(byte)*PTR_CAN21A_RxBuffer_00035774 * 0x100 +
       (ushort)(byte)PTR_CAN21A_RxBuffer_00035774[1];
  *(ushort *)PTR_CAN21A_RawWord1_0003577c =
       (ushort)(byte)puVar1[2] * 0x100 + (ushort)(byte)puVar1[3];
  return;
}

