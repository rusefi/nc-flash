/* Ghidra analysis output; verify against original SH instructions. */

/* 4019+sat_s16(slot2*16), clamp0..15232. Original36A0A/10C4C execute;17boundary cases. Upper
   application clamp15206 can win over this larger lower value. */

int ClassAdjustment_ApplicationLowerLimit(void)

{
  short sVar1;
  short sVar3;
  int iVar2;
  
  sVar3 = (*(code *)PTR_ClassAdjustment_FixedConsumer_000367d8)();
  sVar1 = *(short *)PTR_DAT_000367dc;
  iVar2 = (*(code *)PTR_Arithmetic_SaturatingMultiplyShift_000367e4)
                    (*(undefined2 *)PTR_DAT_000367e0,(int)sVar3,0xf);
  iVar2 = sVar1 + iVar2;
  if (iVar2 < *(short *)PTR_PTR_000367e8) {
    iVar2 = (int)*(short *)PTR_PTR_000367e8;
  }
  if (*(short *)PTR_DAT_000367ec < iVar2) {
    iVar2 = (int)*(short *)PTR_DAT_000367ec;
  }
  return iVar2;
}

