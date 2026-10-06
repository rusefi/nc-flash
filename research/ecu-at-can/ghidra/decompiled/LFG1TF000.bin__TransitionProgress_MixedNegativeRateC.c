/* Ghidra analysis output; verify against original SH instructions. */

/* Unsigneddoubled80FE/FA weightedby770C8/C9
   bytes100/96,divide100,addsigned770CA5018,unsignedcapFFFF;store9708. Curve70B2D
   result>>8*signed9718>>6,negated. */

int TransitionProgress_MixedNegativeRateC(void)

{
  short sVar1;
  ushort extraout_var;
  int iVar2;
  undefined *puVar3;
  
  iVar2 = (*(code *)PTR_FUN_00032c68)
                    (((int)DAT_ffff80fa & 0x7fffU) * 2 *
                     (uint)(byte)*PTR_TransitionProgress_MixedWeightFA_00032c64 +
                     ((int)DAT_ffff80fe & 0x7fffU) * 2 *
                     (uint)(byte)*PTR_TransitionProgress_MixedWeightFE_00032c60,100);
  puVar3 = (undefined *)(iVar2 + *(short *)PTR_TransitionProgress_MixedOffset_00032c6c);
  if (PTR_DAT_00032c70 <
      (undefined *)(iVar2 + *(short *)PTR_TransitionProgress_MixedOffset_00032c6c)) {
    puVar3 = PTR_DAT_00032c70;
  }
  (*(code *)PTR_Lookup_ByteCurveToFixedPoint_00032c5c)
            (puVar3,PTR_TransitionProgress_NegativeCCurve_00032c74);
  sVar1 = *(short *)(int)DAT_00032c4a;
  *(short *)(int)DAT_00032c4c = (short)puVar3;
  return -((int)(short)(extraout_var & 0xff) * (int)sVar1 >> 6);
}

