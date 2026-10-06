/* Ghidra analysis output; verify against original SH instructions. */

/* Packs8 bytes at6B50 when734A has40 or80; otherwise retains payload. Both transmission modes
   publish. No hardware transmission emulated. */

void CAN215_Pack(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined *puVar5;
  undefined4 uVar6;
  
  uVar6 = (*(code *)PTR_FUN_00036b18)(0x10);
  puVar4 = PTR_DAT_00036b30;
  puVar2 = PTR_DAT_00036b24;
  puVar1 = PTR_CAN215_EncodedWord0_00036b20;
  if (((*PTR_TransmissionModeFlags_00036b1c & 0x40) != 0) ||
     (((int)(char)*PTR_TransmissionModeFlags_00036b1c & 0x80U) != 0)) {
    *PTR_DAT_00036b24 = (char)((ushort)*(undefined2 *)PTR_CAN215_EncodedWord0_00036b20 >> 8);
    puVar3 = PTR_DAT_00036b28;
    puVar2[1] = puVar1[1];
    puVar5 = PTR_DAT_00036b34;
    puVar2[2] = (char)((ushort)*(undefined2 *)puVar3 >> 8);
    puVar1 = PTR_CAN215_EncodedWord4_00036b2c;
    puVar2[3] = puVar3[1];
    puVar2[4] = (char)((ushort)*(undefined2 *)puVar1 >> 8);
    puVar2[5] = puVar1[1];
    puVar2[6] = *puVar4;
    puVar2[7] = *puVar5;
  }
  (*(code *)PTR_FUN_00036b38)(uVar6);
  return;
}

