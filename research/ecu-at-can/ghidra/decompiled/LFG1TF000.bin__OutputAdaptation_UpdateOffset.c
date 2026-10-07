/* Ghidra analysis output; verify against original SH instructions. */

/* UnsignedA518 clamp8000..16000 minus8000 indexes five-point row at8AD4+12*i withspacing2000
   andFFFF sentinel; unsignedwordclamp0..32767 into8A44.328 cases and original dispatcher;
   physicalunits unproved. */

void OutputAdaptation_UpdateOffset(byte param_1)

{
  short sVar2;
  undefined4 uVar1;
  undefined2 uVar3;
  int iVar4;
  
  sVar2 = (*(code *)PTR_FUN_00018f04)
                    ((int)*(short *)PTR_DAT_00018f00,(int)DAT_00018ee0,(int)DAT_00018ede);
  uVar1 = (*(code *)PTR_Lookup_UniformWordStep_00018f0c)
                    ((int)(short)(sVar2 + DAT_00018ee2),
                     (uint)param_1 * 0xc + *(int *)PTR_DAT_00018f08,(int)DAT_00018ee4);
  iVar4 = (int)DAT_00018ee6;
  uVar3 = (*(code *)PTR_FUN_00018f04)(uVar1,0,(int)DAT_00018ee8);
  *(undefined2 *)(iVar4 + (uint)param_1 * 2) = uVar3;
  return;
}

