/* Ghidra analysis output; verify against original SH instructions. */

/* 400A through2534 withstockDC47C256 passeswordunchanged
   to40EC;40E8=RTZ(raw/65536*20).1024valid10bitcounts and42boundary/historycases. Boardunitsunknown.
    */

undefined4 * Acquisition_ScaleChannel1(void)

{
  undefined *puVar1;
  ushort uVar2;
  
  uVar2 = (*(code *)PTR_FUN_00006768)
                    (*(undefined2 *)PTR_DAT_0000675c,
                     *(undefined2 *)PTR_Acquisition_Channel1WordHistory_00006760,
                     (int)*(short *)PTR_DAT_00006764);
  puVar1 = PTR_Acquisition_Channel1WordHistory_00006760;
  *(float *)PTR_Acquisition_ScaledChannel1_00006774 =
       ((float)uVar2 / DAT_0000676c) * *(float *)PTR_DAT_00006770;
  *(ushort *)puVar1 = uVar2;
  return &DAT_0000676c;
}

