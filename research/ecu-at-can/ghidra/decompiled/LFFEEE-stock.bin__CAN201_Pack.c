/* Ghidra analysis output; verify against original SH instructions. */

/* First BE word paired with TCU getter1C890; bytes4-5 encode6B38 speed candidate. CAN4B0/CAN216
   paths executed; PRHT consumption unproven. */

void CAN201_Pack(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined *puVar5;
  undefined4 uVar6;
  
  uVar6 = (*(code *)PTR_FUN_000367d4)(0x10);
  puVar4 = PTR_DAT_000367ec;
  puVar2 = PTR_CAN201_TxBuffer_000367e0;
  puVar1 = PTR_DAT_000367dc;
  if (((*PTR_TransmissionModeFlags_000367d8 & 0x40) != 0) ||
     (((int)(char)*PTR_TransmissionModeFlags_000367d8 & 0x80U) != 0)) {
    *PTR_CAN201_TxBuffer_000367e0 = (char)((ushort)*(undefined2 *)PTR_DAT_000367dc >> 8);
    puVar3 = PTR_DAT_000367e4;
    puVar2[1] = puVar1[1];
    puVar5 = PTR_DAT_000367f0;
    puVar2[2] = (char)((ushort)*(undefined2 *)puVar3 >> 8);
    puVar1 = PTR_CAN201_SpeedCandidateWord_000367e8;
    puVar2[3] = puVar3[1];
    puVar2[4] = (char)((ushort)*(undefined2 *)puVar1 >> 8);
    puVar2[5] = puVar1[1];
    puVar2[6] = *puVar4;
    puVar2[7] = *puVar5;
  }
  (*DAT_000367f4)(uVar6);
  return;
}

