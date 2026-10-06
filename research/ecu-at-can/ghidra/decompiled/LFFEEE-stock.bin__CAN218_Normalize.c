/* Ghidra analysis output; verify against original SH instructions. */

/* word0*0.05-200; byte2-50; word4 numeric/sentinel; byte6*2-100 with cap. */

undefined4 CAN218_Normalize(void)

{
  char cVar1;
  bool bVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined *puVar5;
  undefined *puVar6;
  undefined *puVar7;
  char cVar8;
  undefined4 uVar9;
  float fVar10;
  float fVar11;
  undefined4 uVar12;
  undefined4 uVar13;
  
  puVar6 = PTR_DAT_00035320;
  puVar5 = PTR_DAT_0003531c;
  puVar4 = PTR_DAT_00035318;
  puVar3 = PTR_DAT_00035314;
  cVar1 = *PTR_DAT_0003530c;
  bVar2 = (*PTR_TransmissionModeFlags_00035310 & 0x40) == 0;
  if ((bVar2) &&
     (cVar8 = (*(code *)PTR_FUN_00035328)(PTR_ATReceiveConfigurationGate_00035324),
     puVar7 = PTR_DAT_00035330, cVar8 == '\x01')) {
    *(undefined2 *)puVar3 = *(undefined2 *)PTR_DAT_0003532c;
    *puVar4 = *puVar7;
    puVar7 = PTR_DAT_0003533c;
    *puVar6 = *PTR_DAT_00035334;
    *(undefined2 *)puVar7 = *(undefined2 *)PTR_DAT_00035338;
    puVar7 = PTR_DAT_00035348;
    *puVar5 = *PTR_DAT_00035340;
    *puVar7 = *PTR_DAT_00035344;
  }
  else {
    puVar7 = PTR_DAT_0003533c;
    *(undefined2 *)puVar3 = DAT_0003530a;
    *puVar4 = 0x32;
    *puVar6 = 0;
    *(undefined2 *)puVar7 = 0;
    *puVar5 = 0x32;
    *PTR_DAT_00035348 = 0;
  }
  uVar12 = 0;
  if (bVar2) {
    if (((undefined *)(uint)*(ushort *)puVar3 == PTR_DAT_0000fffc_3_00035360) || (cVar1 == '\x01'))
    {
      *(undefined4 *)PTR_CAN218_Field0_0003535c = 0;
    }
    else {
      uVar9 = (*(code *)PTR_FUN_00035358)(DAT_00035368,DAT_00035364);
      *(undefined4 *)PTR_CAN218_Field0_0003535c = uVar9;
    }
  }
  else {
    uVar9 = (*(code *)PTR_FUN_00035358)(DAT_00035350,DAT_0003534c,(int)*(short *)PTR_DAT_00035354);
    *(undefined4 *)PTR_CAN218_Field0_0003535c = uVar9;
  }
  uVar13 = 0x3f800000;
  uVar9 = (*(code *)PTR_FUN_00035370)(0x3f800000,DAT_0003536c,(int)(char)*puVar4);
  *(undefined4 *)PTR_CAN218_Byte2Minus50_00035374 = uVar9;
  if ((*puVar6 & 0x80) == 0) {
    *PTR_DAT_00035378 = 0;
  }
  else {
    *PTR_DAT_00035378 = 1;
  }
  puVar3 = PTR_FUN_0003546c;
  uVar9 = DAT_00035478;
  if ((((undefined *)(uint)*(ushort *)PTR_DAT_00035470 != PTR_DAT_0000fffc_3_00035474) &&
      (cVar1 != '\x01')) && (bVar2)) {
    uVar9 = (*(code *)PTR_FUN_0003547c)(uVar13,uVar12);
  }
  (*(code *)puVar3)(uVar9,PTR_CAN218_Word4Value_00035480);
  if ((((byte)*puVar5 == DAT_00035468) || (cVar1 == '\x01')) ||
     ((!bVar2 || (*PTR_DAT_00035484 == '\x01')))) {
    uVar12 = (*(code *)puVar3)(DAT_00035488,PTR_CAN218_Byte6Request_0003548c);
  }
  else {
    fVar10 = (float)(*(code *)PTR_FUN_00035494)(0x40000000,DAT_00035490);
    fVar11 = *(float *)PTR_DAT_00035498;
    if (fVar10 <= *(float *)PTR_DAT_00035498) {
      fVar11 = fVar10;
    }
    uVar12 = (*(code *)puVar3)(fVar11,PTR_CAN218_Byte6Request_0003548c);
  }
  return uVar12;
}

