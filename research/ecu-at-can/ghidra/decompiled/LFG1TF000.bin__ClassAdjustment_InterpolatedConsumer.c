/* Ghidra analysis output; verify against original SH instructions. */

/* Buildsbytemapaxes28/36/44,ys((stored+136)>>1)&255;10764atu16(2*80EE),decode>>7-136,clamp+/-80,*16.Quantization/spreadovershootconsumerverified.
    */

int ClassAdjustment_InterpolatedConsumer(void)

{
  int iVar1;
  uint uVar2;
  int iVar3;
  int iVar4;
  undefined1 local_1c;
  undefined1 uStack_1b;
  undefined1 uStack_1a;
  undefined1 uStack_19;
  undefined1 auStack_18 [8];
  
  local_1c = 3;
  uStack_1b = (undefined1)
              ((int)((uint)(byte)*PTR_DAT_00036b90 + (uint)(byte)*PTR_DAT_00036b94) >> 1);
  uStack_1a = (undefined1)
              ((int)((uint)(byte)*PTR_DAT_00036b94 + (uint)(byte)*PTR_DAT_00036b98) >> 1);
  iVar3 = (int)DAT_00036b8a;
  iVar4 = 0;
  uStack_19 = (undefined1)
              ((int)((uint)(byte)*PTR_DAT_00036b98 + (uint)(byte)*PTR_DAT_00036b9c) >> 1);
  do {
    iVar1 = ClassAdjustment_ReadStored(iVar4);
    auStack_18[(char)iVar4] = (char)(iVar1 + iVar3 >> 1);
    iVar4 = iVar4 + 1;
  } while (iVar4 < 3);
  uVar2 = (*(code *)PTR_Lookup_ByteCurveToFixedPoint_00036ba0)
                    ((int)Phase_MeasuredSourceSample << 1,&local_1c);
  iVar3 = (int)DAT_00036b8c + ((uVar2 & 0xffff) >> 7);
  if (*(short *)PTR_DAT_00036ba4 < iVar3) {
    iVar3 = (int)*(short *)PTR_DAT_00036ba4;
  }
  if (iVar3 < *(short *)PTR_DAT_00036ba8) {
    iVar3 = (int)*(short *)PTR_DAT_00036ba8;
  }
  return iVar3 << 4;
}

