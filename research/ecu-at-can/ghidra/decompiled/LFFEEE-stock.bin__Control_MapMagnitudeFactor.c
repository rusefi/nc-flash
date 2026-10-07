/* Ghidra analysis output; verify against original SH instructions. */

/* 8110=A36A0(6D28). Eightknots-40..100by20,values0/0/0/0/.1/.4/1/1.
   Originallookupandboundariesverified. */

void Control_MapMagnitudeFactor(void)

{
  undefined4 uVar1;
  
  uVar1 = (*(code *)PTR_FUN_000594b4)(PTR_Control_RawFirstAlternate_000594b0);
  uVar1 = (*(code *)PTR_Lookup_FloatCurve_000594bc)
                    (uVar1,PTR_Control_MagnitudeFactorDescriptor_000594b8);
  *(undefined4 *)PTR_Control_MagnitudeInputFactor_000594c0 = uVar1;
  return;
}

