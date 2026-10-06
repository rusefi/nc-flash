/* Ghidra analysis output; verify against original SH instructions. */

/* Mode-gated decode and validity; word0 minus 512 -> FFFF6A34. */

void CAN216_Normalize(void)

{
  bool bVar1;
  undefined2 uVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined *puVar5;
  undefined *puVar6;
  undefined *puVar7;
  undefined *puVar8;
  char cVar9;
  undefined4 uVar10;
  
  puVar6 = PTR_DAT_00034de4;
  puVar5 = PTR_DAT_00034de0;
  puVar4 = PTR_DAT_00034ddc;
  puVar3 = PTR_DAT_00034dd8;
  bVar1 = (*PTR_TransmissionModeFlags_00034dd4 & 0x40) != 0;
  if ((bVar1) ||
     (cVar9 = (*(code *)PTR_FUN_00034dec)(PTR_ATReceiveConfigurationGate_00034de8),
     puVar7 = PTR_DAT_00034df4, cVar9 != '\x01')) {
    puVar7 = PTR_DAT_00034dfc;
    uVar2 = DAT_00034dce;
    *(undefined2 *)puVar4 = DAT_00034dce;
    *(undefined2 *)puVar3 = uVar2;
    *puVar7 = 0;
    *(undefined2 *)puVar5 = DAT_00034dd0;
    *puVar6 = 0;
  }
  else {
    *(undefined2 *)puVar4 = *(undefined2 *)PTR_DAT_00034df0;
    *(undefined2 *)puVar3 = *(undefined2 *)puVar7;
    *PTR_DAT_00034dfc = *PTR_DAT_00034df8;
    *(undefined2 *)puVar5 = *(undefined2 *)PTR_DAT_00034e00;
    *puVar6 = *PTR_DAT_00034e04;
  }
  puVar7 = PTR_DAT_0000fffc_3_00034e08;
  if ((((undefined *)(uint)*(ushort *)puVar4 == PTR_DAT_0000fffc_3_00034e08) ||
      (*PTR_DAT_00034e0c == '\x01')) || (bVar1)) {
    *(undefined4 *)PTR_CAN216_Word0Minus512_00034e14 = DAT_00034e10;
  }
  else {
    uVar10 = (*(code *)PTR_FUN_00034e1c)(0x3f800000,DAT_00034e18);
    *(undefined4 *)PTR_CAN216_Word0Minus512_00034e14 = uVar10;
  }
  puVar8 = PTR_DAT_00034e24;
  puVar4 = PTR_DAT_00034e20;
  if (*PTR_CAN216_ReceiptCounter_00034e2c == '\0') {
    *(short *)PTR_DAT_00034e28 = (short)puVar7;
    *puVar8 = (char)DAT_00034dd2;
    *(short *)puVar4 = (short)puVar7;
  }
  else {
    *(undefined2 *)PTR_DAT_00034e28 = *(undefined2 *)puVar3;
    *puVar8 = *PTR_DAT_00034dfc;
    *(undefined2 *)puVar4 = *(undefined2 *)puVar5;
  }
  if ((*puVar6 & 0x80) == 0) {
    *PTR_DAT_00034e30 = 0;
  }
  else {
    *PTR_DAT_00034e30 = 1;
  }
  if ((*puVar6 & 0x40) == 0) {
    *PTR_DAT_00034f08 = 0;
  }
  else {
    *PTR_DAT_00034f08 = 1;
  }
  if ((*puVar6 & 0x20) == 0) {
    *PTR_CAN216_Bit5CutRequest_00034f0c = 0;
  }
  else {
    *PTR_CAN216_Bit5CutRequest_00034f0c = 1;
  }
  if ((*puVar6 & 0x10) == 0) {
    *PTR_DAT_00034f10 = 0;
  }
  else {
    *PTR_DAT_00034f10 = 1;
  }
  if ((*puVar6 & 8) == 0) {
    *PTR_DAT_00034f14 = 0;
  }
  else {
    *PTR_DAT_00034f14 = 1;
  }
  if ((*puVar6 & 4) == 0) {
    *PTR_DAT_00034f18 = 0;
  }
  else {
    *PTR_DAT_00034f18 = 1;
  }
  (*(code *)PTR_FUN_00034f20)(PTR_DAT_00034f1c,(*puVar6 & 2) != 0);
  return;
}

