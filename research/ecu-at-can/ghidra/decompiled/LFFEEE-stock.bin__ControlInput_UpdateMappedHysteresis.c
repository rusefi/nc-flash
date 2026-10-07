/* Ghidra analysis output; verify against original SH instructions. */

/* 693Dclear below mapA37E0(6D20)-mapA37EC;set strictlyabove firstmap whenDB0B9exact1(stock1),else
   retainrawbyte.2196cases. Upper equality retains, unlike307EC. */

uint ControlInput_UpdateMappedHysteresis(void)

{
  uint uVar1;
  float fVar2;
  undefined4 uVar3;
  float fVar4;
  float extraout_fr0;
  
  fVar2 = (float)(*(code *)PTR_FUN_00030cb4)(PTR_DAT_00030cb0);
  uVar3 = (*(code *)PTR_FUN_00030cb4)(PTR_Control_RawFirstPublished_00030cb8);
  fVar4 = (float)(*(code *)PTR_Lookup_FloatCurve_00030cc0)(uVar3,PTR_PTR_00030cbc);
  uVar1 = (*(code *)PTR_Lookup_FloatCurve_00030cc0)(uVar3,PTR_PTR_00030cc4);
  if (fVar4 - extraout_fr0 <= fVar2) {
    if ((fVar4 < fVar2) && (uVar1 = (uint)(byte)*PTR_DAT_00030ccc, uVar1 == 1)) {
      *PTR_ControlInput_MappedHysteresisGate_00030cc8 = 1;
    }
  }
  else {
    *PTR_ControlInput_MappedHysteresisGate_00030cc8 = 0;
  }
  return uVar1;
}

