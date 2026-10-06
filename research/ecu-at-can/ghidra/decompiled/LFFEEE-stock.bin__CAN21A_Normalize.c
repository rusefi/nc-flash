/* Ghidra analysis output; verify against original SH instructions. */

/* Executed: word0 minus10000 floor-1000; word1 minus10000 cap10000 gated by any CAN211 request
   and7190!=1. Receipt/sentinels ->-10000; FFFE special only word1. See traction-flags.txt. */

undefined4 CAN21A_Normalize(void)

{
  char cVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined *puVar5;
  undefined4 uVar6;
  float fVar7;
  float fVar8;
  undefined4 uVar9;
  
  puVar5 = PTR_CAN21A_Word0Value_000356c8;
  puVar4 = PTR_CAN21A_ReceiptCounter_000356c4;
  puVar3 = PTR_CAN21A_RawWord1_000356bc;
  puVar2 = PTR_DAT_000356b4;
  uVar9 = 0x3f800000;
  *(undefined2 *)PTR_DAT_000356b4 = *(undefined2 *)PTR_CAN21A_RawWord0_000356b8;
  *(undefined2 *)PTR_DAT_000356c0 = *(undefined2 *)puVar3;
  uVar6 = DAT_000356cc;
  cVar1 = *puVar4;
  if ((*(ushort *)puVar2 == DAT_000356d0) || (cVar1 == '\0')) {
    *(undefined4 *)puVar5 = DAT_000356cc;
  }
  else {
    fVar7 = (float)(*(code *)PTR_FUN_000356d4)(0x3f800000,DAT_000356cc);
    if (fVar7 <= *(float *)PTR_DAT_000356d8) {
      *(float *)puVar5 = *(float *)PTR_DAT_000356d8;
    }
    else {
      *(float *)puVar5 = fVar7;
    }
  }
  puVar2 = PTR_FUN_000356dc;
  if ((((*(ushort *)PTR_DAT_000356c0 == DAT_000356d0) || (cVar1 == '\0')) ||
      (*PTR_DAT_000356e0 == '\x01')) ||
     ((((*PTR_DAT_000356e4 == '\0' && (*PTR_DAT_000356e8 == '\0')) &&
       ((*PTR_DAT_000356ec == '\0' && ((*PTR_DAT_000356f0 == '\0' && (*PTR_DAT_000356f4 == '\0')))))
       ) || (*(ushort *)PTR_DAT_000356c0 == DAT_000356f8)))) {
    uVar6 = (*(code *)PTR_FUN_000356dc)(uVar6,PTR_CAN21A_GatedWord1Value_000356fc);
  }
  else {
    fVar8 = (float)(*(code *)PTR_FUN_000356d4)(uVar9,uVar6);
    fVar7 = *(float *)PTR_DAT_00035700;
    if (fVar8 < *(float *)PTR_DAT_00035700) {
      fVar7 = fVar8;
    }
    uVar6 = (*(code *)puVar2)(fVar7,PTR_CAN21A_GatedWord1Value_000356fc);
  }
  return uVar6;
}

