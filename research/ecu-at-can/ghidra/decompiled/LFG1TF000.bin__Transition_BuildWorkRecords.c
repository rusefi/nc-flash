/* Ghidra analysis output; verify against original SH instructions. */

/* Executedafteracceptedindexchange. MOVA/BRAF48F58/5C jump table; calls4C100 forrecordpointer,
   writestransition/indexmetadata, calls31524. Fullphysicalactuator meaning unproved;
   newrelative-branch ISA tests. */

undefined * Transition_BuildWorkRecords(void)

{
  byte bVar1;
  byte bVar2;
  byte bVar3;
  undefined *puVar4;
  undefined *puVar5;
  undefined *puVar6;
  ushort *puVar7;
  undefined *puVar8;
  uint uVar9;
  uint uVar10;
  uint uVar11;
  byte *pbVar12;
  uint uVar13;
  
  puVar5 = PTR_EventMessage_NextBuffer_00048f74;
  puVar4 = PTR_Phase_DispatchEvent_00048f70;
  bVar1 = *(byte *)(int)DAT_00048f60;
  bVar3 = PTR_DAT_00048f64[bVar1];
  uVar11 = (uint)(char)bVar3;
  bVar2 = *PTR_DAT_00048f6c;
  puVar6 = (undefined *)(uint)bVar1;
  pbVar12 = (byte *)(int)DAT_00048f62;
  switch(puVar6) {
  case (undefined *)0x0:
  case (undefined *)0x1:
  case (undefined *)0x2:
  case (undefined *)0x3:
  case (undefined *)0x4:
  case (undefined *)0x5:
  case (undefined *)0x6:
  case (undefined *)0x7:
  case (undefined *)0x8:
  case (undefined *)0x9:
  case (undefined *)0xa:
  case (undefined *)0xb:
    puVar7 = (ushort *)(*(code *)PTR_EventMessage_NextBuffer_00048f74)();
    *puVar7 = (ushort)*(byte *)(int)DAT_00049056;
    puVar7[1] = (ushort)*pbVar12;
    puVar7[2] = (ushort)bVar2;
    puVar6 = (undefined *)(*(code *)puVar4)(1);
    break;
  default:
    uVar13 = (uint)(byte)PTR_DAT_00048f68[bVar1];
    if (uVar13 < bVar3) {
      puVar8 = PTR_DAT_00049058 + (uint)bVar3 * 6;
      uVar10 = (uint)bVar3;
      puVar6 = PTR_DAT_00049058;
      uVar9 = uVar10;
      while (uVar9 != uVar13) {
        uVar10 = uVar10 - 1;
        bVar1 = puVar8[uVar10];
        puVar7 = (ushort *)(*(code *)puVar5)();
        *puVar7 = (ushort)bVar1;
        puVar7[1] = (ushort)*pbVar12;
        puVar7[2] = (ushort)bVar2;
        puVar6 = (undefined *)(*(code *)puVar4)(1);
        uVar11 = uVar11 - 1;
        puVar8 = puVar8 + -6;
        uVar9 = uVar11 & 0xff;
      }
    }
    else {
      uVar10 = (uint)bVar3;
      while (uVar10 != uVar13) {
        bVar1 = PTR_DAT_00049058[(uVar11 & 0xff) + (uVar11 & 0xff) * 6 + 1];
        puVar7 = (ushort *)(*(code *)puVar5)();
        *puVar7 = (ushort)bVar1;
        puVar7[1] = (ushort)*pbVar12;
        puVar7[2] = (ushort)bVar2;
        puVar6 = (undefined *)(*(code *)puVar4)(1);
        uVar11 = uVar11 + 1;
        uVar10 = uVar11 & 0xff;
      }
    }
  }
  return puVar6;
}

