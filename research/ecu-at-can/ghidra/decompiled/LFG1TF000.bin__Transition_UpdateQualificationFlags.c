/* Ghidra analysis output; verify against original SH instructions. */

/* limit9C52=max(u16 939E,ROM7734A9600). Low9C54 bits from75144(x,z),75166(y),75155(z,y)>=limit or
   respective source==25600; x/y/z96C8/CA/CC. Preserves high5bits;1372 original-map cases. */

void Transition_UpdateQualificationFlags(void)

{
  ushort uVar1;
  ushort uVar2;
  bool bVar3;
  bool bVar4;
  bool bVar5;
  ushort uVar6;
  ushort uVar7;
  byte bVar8;
  ushort uVar9;
  byte *pbVar10;
  
  uVar9 = *(ushort *)PTR_DAT_000475b4;
  if (uVar9 < *(ushort *)PTR_Transition_MinimumQualificationLimit_000475b8) {
    uVar9 = *(ushort *)PTR_Transition_MinimumQualificationLimit_000475b8;
  }
  *(ushort *)(int)DAT_000475ae = uVar9;
  uVar7 = *(ushort *)PTR_TransitionProgress_AccumulatorA_000475bc;
  uVar1 = *(ushort *)PTR_TransitionProgress_AccumulatorB_000475c0;
  uVar2 = *(ushort *)PTR_TransitionProgress_AccumulatorC_000475c4;
  pbVar10 = (byte *)(int)DAT_000475b0;
  uVar6 = (*(code *)PTR_Lookup_ByteGrid2D_Q8_000475cc)
                    ((int)(short)uVar7,(int)(short)uVar2,PTR_Transition_QualificationMap0_000475c8);
  if ((uVar6 < uVar9) && ((uint)uVar7 != (int)DAT_000475b2)) {
    bVar5 = false;
  }
  else {
    bVar5 = true;
  }
  uVar7 = (*(code *)PTR_Lookup_ByteCurveToFixedPoint_000475d4)
                    ((int)(short)uVar1,PTR_Transition_QualificationCurve1_000475d0);
  if ((uVar7 < uVar9) && ((uint)uVar1 != (int)DAT_000475b2)) {
    bVar3 = false;
  }
  else {
    bVar3 = true;
  }
  uVar7 = (*(code *)PTR_Lookup_ByteGrid2D_Q8_000475cc)
                    ((int)(short)uVar2,(int)(short)uVar1,PTR_Transition_QualificationMap2_000475d8);
  if ((uVar7 < uVar9) && ((uint)uVar2 != (int)DAT_000475b2)) {
    bVar4 = false;
  }
  else {
    bVar4 = true;
  }
  if (bVar5) {
    bVar8 = *pbVar10 | 1;
  }
  else {
    bVar8 = *pbVar10 & 0xfe;
  }
  *pbVar10 = bVar8;
  if (bVar3) {
    bVar8 = *pbVar10 | 2;
  }
  else {
    bVar8 = *pbVar10 & 0xfd;
  }
  *pbVar10 = bVar8;
  if (bVar4) {
    bVar8 = *pbVar10 | 4;
  }
  else {
    bVar8 = *pbVar10 & 0xfb;
  }
  *pbVar10 = bVar8;
  return;
}

