/* Ghidra analysis output; verify against original SH instructions. */

/* Byte layout verified against actual LFG1TF000 packers. */

void CAN218_Unpack(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  
  puVar2 = PTR_DAT_000354a4;
  puVar1 = PTR_CAN218_RxBuffer_0003549c;
  *(ushort *)PTR_DAT_000354a0 =
       (ushort)(byte)*PTR_CAN218_RxBuffer_0003549c * 0x100 +
       (ushort)(byte)PTR_CAN218_RxBuffer_0003549c[1];
  *puVar2 = puVar1[2];
  puVar3 = PTR_DAT_000354b4;
  *PTR_DAT_000354a8 = puVar1[3];
  puVar2 = PTR_DAT_000354b0;
  *(ushort *)PTR_DAT_000354ac = (ushort)(byte)puVar1[4] * 0x100 + (ushort)(byte)puVar1[5];
  *puVar2 = puVar1[6];
  *puVar3 = puVar1[7];
  return;
}

