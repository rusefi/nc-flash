/* Ghidra analysis output; verify against original SH instructions. */

/* 682C clamp0..1 of(6DB4-mapA37E0)/(7020-mapA37E0), finiteRTZ. Hold old whenabsolute
   denominator<=~1e-5.4575cases andcaller/retained coupling. Units unproved. */

uint ControlInput_NormalizeLimitRatio(void)

{
  uint uVar1;
  undefined4 uVar2;
  float fVar3;
  float fVar4;
  undefined4 extraout_fr0;
  float fVar5;
  
  uVar2 = (*(code *)PTR_FUN_00031878)(PTR_Control_RawFirstPublished_00031874);
  fVar3 = (float)(*(code *)PTR_Lookup_FloatCurve_00031880)(uVar2,PTR_PTR_0003187c);
  uVar2 = 0;
  fVar5 = *(float *)PTR_DAT_00031884 - fVar3;
  uVar1 = (*(code *)PTR_FUN_0003188c)(fVar5,0,DAT_00031888);
  if ((uVar1 & 0xff) != 0) {
    fVar4 = (float)(*(code *)PTR_FUN_00031878)(PTR_DAT_00031890);
    uVar1 = (*(code *)PTR_FUN_00031894)((fVar4 - fVar3) / fVar5,uVar2,0x3f800000);
    *(undefined4 *)PTR_ControlInput_NormalizedLimitRatio_00031898 = extraout_fr0;
  }
  return uVar1;
}

