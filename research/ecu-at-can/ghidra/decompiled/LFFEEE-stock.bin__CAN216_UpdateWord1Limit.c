/* Ghidra analysis output; verify against original SH instructions. */

/* Second word recovery and sentinel logic -> FFFF6A30; physical role under investigation. */

uint CAN216_UpdateWord1Limit(void)

{
  byte bVar1;
  undefined *puVar2;
  uint uVar3;
  undefined4 extraout_fr0;
  undefined4 extraout_fr0_00;
  undefined4 uVar4;
  undefined4 extraout_fr0_01;
  float fVar5;
  
  puVar2 = PTR_CAN216_Word1Limit_00034f34;
  fVar5 = *(float *)PTR_CAN216_Word1Limit_00034f34;
  if (((*PTR_DAT_00034f38 == '\x01') || (*PTR_CAN216_ReceiptCounter_00034f3c == '\0')) ||
     (((byte)*PTR_DAT_00034f40 & 0xf0) == DAT_00034f06)) {
    uVar3 = (*(code *)PTR_FUN_00034f48)
                      (fVar5 + *(float *)PTR_DAT_00034f30,*(undefined4 *)PTR_DAT_00034f44);
    uVar4 = extraout_fr0;
  }
  else {
    uVar3 = -(((*PTR_TransmissionModeFlags_00035088 & 0x40) == 0) - 1);
    if ((((uVar3 == 1) ||
         ((undefined *)(uint)*(ushort *)PTR_DAT_0003508c == PTR_DAT_0000fffc_3_00035090)) ||
        (((uVar3 = 1, *PTR_DAT_00035094 == '\x01' ||
          (uVar3 = (uint)(byte)*PTR_DAT_00035098, uVar3 == 1)) &&
         (*(float *)PTR_DAT_00034f28 - *(float *)PTR_Model_RatioOffset_00034f24 < fVar5)))) ||
       (*PTR_DAT_0003509c != '\0')) {
      *(undefined4 *)PTR_CAN216_Word1Limit_00034f34 = DAT_00035084;
      return uVar3;
    }
    if ((*PTR_DAT_00035094 != '\x01') && (bVar1 = *PTR_DAT_00035098, bVar1 != 1)) {
      if ((*(ushort *)PTR_DAT_000350a4 <= *(ushort *)PTR_DAT_00034f2c) &&
         (*(ushort *)PTR_DAT_00034f2c <= *(ushort *)PTR_DAT_000350a8)) {
        *(undefined4 *)PTR_CAN216_Word1Limit_00034f34 = *(undefined4 *)PTR_DAT_000350ac;
        return (uint)bVar1;
      }
      uVar3 = (*DAT_000350b4)(0x3f800000,DAT_000350b0);
      *(undefined4 *)puVar2 = extraout_fr0_01;
      return uVar3;
    }
    uVar3 = (*(code *)PTR_FUN_000350a0)(fVar5 + *(float *)PTR_DAT_00034f30,DAT_00035084);
    uVar4 = extraout_fr0_00;
  }
  *(undefined4 *)puVar2 = uVar4;
  return uVar3;
}

