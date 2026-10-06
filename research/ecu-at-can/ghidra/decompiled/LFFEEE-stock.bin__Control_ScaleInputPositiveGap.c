/* Ghidra analysis output; verify against original SH instructions. */

/* Mode1 scales805C*6DB4 /60 *CC028 *CA974 /2 into8058 withRTZ eachoperation;elsezero. */

undefined4 * Control_ScaleInputPositiveGap(void)

{
  uint uVar1;
  undefined4 *puVar2;
  float fVar3;
  
  uVar1 = (*(code *)PTR_FUN_00058914)(PTR_DAT_00058954);
  puVar2 = (undefined4 *)(uVar1 & 0xff);
  if (puVar2 == (undefined4 *)0x1) {
    fVar3 = (float)(*(code *)PTR_FUN_00058930)(PTR_DAT_0005892c);
    puVar2 = &DAT_0005897c;
    *(float *)PTR_Control_ScaledPositiveInputGap_00058988 =
         (((*(float *)PTR_Control_PositiveInputGap_00058978 * fVar3) / DAT_0005897c) *
          *(float *)PTR_DAT_00058980 * *(float *)PTR_DAT_00058984) / 2.0;
  }
  else {
    *(undefined4 *)PTR_Control_ScaledPositiveInputGap_00058988 = 0;
  }
  return puVar2;
}

