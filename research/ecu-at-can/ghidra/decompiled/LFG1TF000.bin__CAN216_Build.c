/* Ghidra analysis output; verify against original SH instructions. */

/* Sources FFFF915A and GBR+BC: (signed16 >>5)+512, lower bound0. Source7FFF or mode0 -> FFFE;
   mode16 -> FFFF. */

void CAN216_Build(ushort param_1)

{
  ushort uVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *unaff_r14;
  
  uVar1 = param_1 & 0xff;
  puVar2 = PTR_DAT_00019018;
  puVar3 = PTR_DAT_00019018;
  if ((uVar1 != 0) && (puVar2 = PTR_DAT_0001901c, puVar3 = PTR_DAT_0001901c, uVar1 != 0x10)) {
    if (uVar1 != 1) goto LAB_00018f74;
    puVar2 = PTR_DAT_00019018;
    if ((int)*(short *)PTR_CAN216_NumericRequestSource_00019020 != (int)DAT_00019008) {
      puVar2 = (undefined *)
               ((int)DAT_0001900a + ((int)*(short *)PTR_CAN216_NumericRequestSource_00019020 >> 5));
    }
    if ((int)puVar2 < 0) {
      puVar2 = (undefined *)0x0;
    }
    puVar3 = PTR_DAT_00019018;
    if ((int)DAT_ffff80bc != (int)DAT_00019008) {
      puVar3 = (undefined *)((int)DAT_0001900a + ((int)DAT_ffff80bc >> 5));
    }
    if ((int)puVar3 < 0) {
      puVar3 = (undefined *)0x0;
    }
  }
  param_1 = (ushort)puVar2;
  unaff_r14 = puVar3;
LAB_00018f74:
  *(ushort *)(int)DAT_0001900c = param_1;
  puVar2 = PTR_CAN216_SetWord0_00019024;
  *(short *)(int)DAT_0001900e = (short)unaff_r14;
  (*(code *)puVar2)();
  (*(code *)PTR_CAN216_SetWord2_00019028)(unaff_r14);
  return;
}

