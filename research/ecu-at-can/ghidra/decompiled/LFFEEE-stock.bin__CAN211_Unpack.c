/* Ghidra analysis output; verify against original SH instructions. */

/* BE bytes0-1 ->6A2A; BE bytes4-5 ->6A2C. Original code executed. DSC sender attribution remains a
   hypothesis. */

void CAN211_Unpack(void)

{
  undefined *puVar1;
  
  puVar1 = PTR_DAT_00034be4;
  *(ushort *)PTR_DAT_00034be8 =
       (ushort)(byte)*PTR_DAT_00034be4 * 0x100 + (ushort)(byte)PTR_DAT_00034be4[1];
  *(ushort *)PTR_DAT_00034bec = (ushort)(byte)puVar1[4] * 0x100 + (ushort)(byte)puVar1[5];
  return;
}

