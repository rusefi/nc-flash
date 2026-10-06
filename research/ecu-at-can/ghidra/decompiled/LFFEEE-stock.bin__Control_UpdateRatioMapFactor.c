/* Ghidra analysis output; verify against original SH instructions. */

/* Fullcaller51286sum,39FB4protected6D4C,thenA35B0lookup->8038.
   Stockall8values1;580casesandserialcycles. Sideoutputs stillcomputed. */

void Control_UpdateRatioMapFactor(void)

{
  undefined4 uVar1;
  
  (*(code *)PTR_Control_SumRatioMapContributions_000585bc)();
  (*(code *)PTR_Control_MapRatioEnvironmentDifference_000585c0)();
  uVar1 = (*(code *)PTR_FUN_000585a0)(PTR_Control_ProtectedMapDifference_000585c4);
  uVar1 = (*(code *)PTR_Lookup_FloatCurve_000585cc)
                    (uVar1,PTR_Control_RatioFactorMapDescriptor_000585c8);
  *(undefined4 *)PTR_Control_RatioMapFactor_00058568 = uVar1;
  return;
}

