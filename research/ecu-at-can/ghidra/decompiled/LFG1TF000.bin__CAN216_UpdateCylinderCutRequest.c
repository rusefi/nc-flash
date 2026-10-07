/* Ghidra analysis output; verify against original SH instructions. */

/* 80E8/703C0 curve, hysteresis1280, selector/timer gates ->9454.800 directcases plus160
   nativewholeRAM returns: communicationinhibit clears beforecall290, but828B/82A7=146>=61 forces0.
   Executes everyevenpair, return1E7AE, notonlyphase2/6. tcu-recovery-cut.txt. */

void CAN216_UpdateCylinderCutRequest(void)

{
  bool bVar1;
  bool bVar2;
  int iVar3;
  char cVar5;
  uint uVar4;
  byte bVar6;
  byte bVar7;
  byte *pbVar8;
  undefined1 uVar9;
  
  bVar1 = (PTR_Selector_ApplicationFlags16_00025098[1] & 4) == 0;
  bVar2 = (*PTR_Selector_ApplicationFlags16_00025098 & 4) == 0;
  bVar7 = *PTR_DAT_0002509c & 1;
  iVar3 = (int)CAN201_Word0ApplicationValue;
  cVar5 = CAN216_AdmitCylinderCutRequest();
  if ((bVar1) && ((*(byte *)(int)DAT_00025096 & 1) == 1)) {
    *PTR_DAT_000250a0 = 0;
  }
  if ((bVar2) && ((*(byte *)(int)DAT_00025096 & 2) != 0)) {
    *PTR_DAT_000250a4 = 0;
  }
  if ((bVar7 == 0) && ((*(byte *)(int)DAT_00025096 & 4) != 0)) {
    *PTR_DAT_000250a8 = 0;
  }
  if (cVar5 == '\x01') {
    uVar4 = (*(code *)PTR_Lookup_ByteCurveToFixedPoint_000250b4)
                      ((int)*(short *)PTR_CutLookup_Axis_000250b0,PTR_DAT_000250ac);
    uVar9 = *PTR_CAN216_CylinderCutRequestSource_000250bc;
    if (((((byte)*PTR_DAT_000250c0 <= (byte)*PTR_DAT_000250c4) ||
         ((byte)*PTR_DAT_000250a8 <= (byte)*PTR_DAT_000250c4)) &&
        ((int)((int)*(short *)PTR_DAT_000250b8 + (uVar4 & 0xffff)) <= iVar3)) &&
       ((((DAT_ffff800e < (byte)*PTR_DAT_000250c8 ||
          ((byte)*PTR_DAT_000250a0 <= (byte)*PTR_DAT_000250cc)) ||
         ((byte)*PTR_DAT_000250a4 <= (byte)*PTR_DAT_000250d0)) && (bVar7 == 0)))) {
      uVar9 = 1;
    }
    if ((((byte)*PTR_DAT_000250c0 < (byte)*PTR_DAT_000250d4) ||
        ((byte)*PTR_DAT_000250a8 < (byte)*PTR_DAT_000250d4)) &&
       (((*PTR_DAT_00025170 & 8) == 0 && ((int)(uVar4 & 0xffff) <= iVar3)))) goto LAB_000250f4;
  }
  uVar9 = 0;
LAB_000250f4:
  pbVar8 = (byte *)(int)DAT_0002516e;
  if (bVar1) {
    bVar6 = *pbVar8 & 0xfe;
  }
  else {
    bVar6 = *pbVar8 | 1;
  }
  *pbVar8 = bVar6;
  if (bVar2) {
    bVar6 = *pbVar8 & 0xfd;
  }
  else {
    bVar6 = *pbVar8 | 2;
  }
  *pbVar8 = bVar6;
  if (bVar7 == 0) {
    bVar7 = *pbVar8 & 0xfb;
  }
  else {
    bVar7 = *pbVar8 | 4;
  }
  *pbVar8 = bVar7;
  *PTR_CAN216_CylinderCutRequestSource_00025174 = uVar9;
  return;
}

