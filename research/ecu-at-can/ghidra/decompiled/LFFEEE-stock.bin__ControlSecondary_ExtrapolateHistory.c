/* Ghidra analysis output; verify against original SH instructions. */

/* 6844 clamp0..3.75 of(6840-DB1AC*old6974)/(1-DB1AC);6974=entry6840. StockDB1AC~.95911;36cases.
   Nonstockzero-divisor branch untested. */

uint ControlSecondary_ExtrapolateHistory(void)

{
  uint uVar1;
  undefined4 extraout_fr0;
  undefined4 uVar2;
  float fVar3;
  float fVar4;
  
  uVar2 = 0;
  fVar4 = 1.0 - *(float *)PTR_DAT_00031a38;
  fVar3 = *(float *)PTR_ControlSecondary_FilteredTarget_00031a30;
  uVar1 = (*(code *)PTR_FUN_000319fc)(fVar4,0,DAT_00031a3c);
  if ((uVar1 & 0xff) != 0) {
    uVar1 = (*(code *)PTR_FUN_00031a44)
                      ((fVar3 - *(float *)PTR_DAT_00031a38 *
                                *(float *)PTR_ControlSecondary_PreviousFilteredTarget_00031a40) /
                       fVar4,uVar2,
                       *(undefined4 *)
                        (PTR_DAT_00031a08 +
                        ((int)(char)*PTR_DAT_00031a04 + (int)DAT_000319ec & 0xffU) * 4));
    *(undefined4 *)PTR_ControlSecondary_ExtrapolatedTarget_00031a48 = extraout_fr0;
  }
  *(float *)PTR_ControlSecondary_PreviousFilteredTarget_00031a40 = fVar3;
  return uVar1;
}

