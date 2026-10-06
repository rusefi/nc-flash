/* Ghidra analysis output; verify against original SH instructions. */

/* High nibble1..6 -> six flags; low nibble0..6 -> seven flags. Exhaustively verified. */

uint CAN231_NormalizeState(void)

{
  char cVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined *puVar5;
  undefined *puVar6;
  uint uVar7;
  byte bVar8;
  undefined4 local_24;
  
  if (((int)(char)*PTR_TransmissionModeFlags_00035a5c & 0x40U) != 0) {
    return (int)(char)*PTR_TransmissionModeFlags_00035a5c;
  }
  uVar7 = (*(code *)PTR_FUN_00035a64)(PTR_ATReceiveConfigurationGate_00035a60);
  puVar2 = PTR_CAN231_WorkingDiscreteByte_00035a70;
  if ((uVar7 & 0xff) != 1) {
    return uVar7 & 0xff;
  }
  *PTR_DAT_00035a6c = *PTR_DAT_00035a68;
  puVar3 = PTR_DAT_00035a7c;
  *puVar2 = *PTR_DAT_00035a74;
  puVar4 = PTR_DAT_00035a80;
  *(undefined2 *)puVar3 = *(undefined2 *)PTR_DAT_00035a78;
  puVar6 = PTR_FUN_00035a8c;
  puVar5 = PTR_FUN_00035a88;
  puVar3 = PTR_DAT_00035a84;
  uVar7 = (int)(char)*PTR_DAT_00035a6c & 0xf0;
  if (uVar7 == 0x10) {
    local_24 = (*(code *)PTR_FUN_00035a88)(0x10);
    *puVar3 = 1;
    *puVar4 = 0;
    puVar3 = PTR_DAT_00035a94;
    *PTR_DAT_00035a90 = 0;
    *puVar3 = 0;
    puVar3 = PTR_DAT_00035a9c;
    *PTR_DAT_00035a98 = 0;
    *puVar3 = 0;
  }
  else if (uVar7 == 0x20) {
    local_24 = (*(code *)PTR_FUN_00035a88)(0x10);
    *puVar3 = 0;
    *puVar4 = 1;
    *PTR_DAT_00035a90 = 0;
    *PTR_DAT_00035a94 = 0;
    *PTR_DAT_00035a98 = 0;
    *PTR_DAT_00035a9c = 0;
  }
  else if (uVar7 == 0x30) {
    local_24 = (*(code *)PTR_FUN_00035a88)(0x10);
    *puVar3 = 0;
    *puVar4 = 0;
    puVar3 = PTR_DAT_00035a94;
    *PTR_DAT_00035a90 = 1;
    *puVar3 = 0;
    puVar3 = PTR_DAT_00035a9c;
    *PTR_DAT_00035a98 = 0;
    *puVar3 = 0;
  }
  else if (uVar7 == 0x40) {
    local_24 = (*(code *)PTR_FUN_00035a88)(0x10);
    *puVar3 = 0;
    *puVar4 = 0;
    *PTR_DAT_00035a90 = 0;
    *PTR_DAT_00035a94 = 1;
    *PTR_DAT_00035a98 = 0;
    *PTR_DAT_00035a9c = 0;
  }
  else if (uVar7 == 0x50) {
    local_24 = (*(code *)PTR_FUN_00035a88)(0x10);
    *puVar3 = 0;
    *puVar4 = 0;
    puVar3 = PTR_DAT_00035a94;
    *PTR_DAT_00035a90 = 0;
    *puVar3 = 0;
    puVar3 = PTR_DAT_00035a9c;
    *PTR_DAT_00035a98 = 1;
    *puVar3 = 0;
  }
  else if (uVar7 == 0x60) {
    local_24 = (*(code *)PTR_FUN_00035a88)(0x10);
    *puVar3 = 0;
    *puVar4 = 0;
    *PTR_DAT_00035a90 = 0;
    *PTR_DAT_00035a94 = 0;
    *PTR_DAT_00035a98 = 0;
    *PTR_DAT_00035a9c = 1;
  }
  else {
    local_24 = (*(code *)PTR_FUN_00035a88)(0x10);
    *puVar3 = 0;
    *puVar4 = 0;
    puVar3 = PTR_DAT_00035a94;
    *PTR_DAT_00035a90 = 0;
    *puVar3 = 0;
    puVar3 = PTR_DAT_00035a9c;
    *PTR_DAT_00035a98 = 0;
    *puVar3 = 0;
  }
  (*(code *)puVar6)(local_24);
  puVar4 = PTR_DAT_00035aa4;
  puVar3 = PTR_DAT_00035aa0;
  bVar8 = *PTR_DAT_00035a6c & 0xf;
  if (bVar8 == 0) {
    local_24 = (*(code *)puVar5)(0x10);
    *PTR_DAT_00035aa8 = 1;
    *PTR_DAT_00035aac = 0;
    *puVar4 = 0;
    *puVar3 = 0;
    *PTR_DAT_00035ab0 = 0;
    *PTR_DAT_00035ab4 = 0;
  }
  else if (bVar8 == 1) {
    local_24 = (*(code *)puVar5)(0x10);
    puVar5 = PTR_DAT_00035aac;
    *PTR_DAT_00035aa8 = 0;
    *puVar5 = 1;
    *puVar4 = 0;
    *puVar3 = 0;
    puVar3 = PTR_DAT_00035ab4;
    *PTR_DAT_00035ab0 = 0;
    *puVar3 = 0;
  }
  else if (bVar8 == 2) {
    local_24 = (*(code *)puVar5)(0x10);
    *PTR_DAT_00035aa8 = 0;
    *PTR_DAT_00035aac = 0;
    *puVar4 = 1;
    *puVar3 = 0;
    *PTR_DAT_00035ab0 = 0;
    *PTR_DAT_00035ab4 = 0;
  }
  else if (bVar8 == 3) {
    local_24 = (*(code *)puVar5)(0x10);
    puVar5 = PTR_DAT_00035be8;
    *PTR_DAT_00035be4 = 0;
    *puVar5 = 0;
    *puVar4 = 0;
    *puVar3 = 1;
    puVar3 = PTR_DAT_00035bf0;
    *PTR_DAT_00035bec = 0;
    *puVar3 = 0;
  }
  else if (bVar8 == 4) {
    local_24 = (*(code *)puVar5)(0x10);
    *PTR_DAT_00035be4 = 0;
    *PTR_DAT_00035be8 = 0;
    *puVar4 = 0;
    *puVar3 = 0;
    *PTR_DAT_00035bec = 1;
    *PTR_DAT_00035bf0 = 0;
  }
  else if (bVar8 == 5) {
    local_24 = (*(code *)puVar5)(0x10);
    puVar5 = PTR_DAT_00035be8;
    *PTR_DAT_00035be4 = 0;
    *puVar5 = 0;
    *puVar4 = 0;
    *puVar3 = 0;
    puVar3 = PTR_DAT_00035bf0;
    *PTR_DAT_00035bec = 0;
    *puVar3 = 1;
  }
  else {
    if (bVar8 == 6) {
      local_24 = (*(code *)puVar5)(0x10);
      *PTR_DAT_00035be4 = 0;
      *PTR_DAT_00035be8 = 0;
      *puVar4 = 0;
      *puVar3 = 0;
      *PTR_DAT_00035bec = 0;
      *PTR_DAT_00035bf0 = 0;
      *PTR_DAT_00035bf4 = 1;
      goto LAB_00035b50;
    }
    local_24 = (*(code *)puVar5)(0x10);
    *PTR_DAT_00035be4 = 0;
    *PTR_DAT_00035be8 = 0;
    *puVar4 = 0;
    *puVar3 = 0;
    *PTR_DAT_00035bec = 0;
    *PTR_DAT_00035bf0 = 0;
  }
  *PTR_DAT_00035bf4 = 0;
LAB_00035b50:
  (*(code *)puVar6)(local_24);
  if (((int)(char)*puVar2 & 0x80U) == 0) {
    *PTR_DAT_00035bf8 = 0;
  }
  else {
    *PTR_DAT_00035bf8 = 1;
  }
  if ((*puVar2 & 0x10) == 0) {
    *PTR_DAT_00035bfc = 0;
  }
  else {
    *PTR_DAT_00035bfc = 1;
  }
  cVar1 = *puVar2;
  if (((int)cVar1 & 8U) == 0) {
    *PTR_DAT_00035c00 = 0;
  }
  else {
    *PTR_DAT_00035c00 = 1;
  }
  return (int)cVar1 & 8U;
}

