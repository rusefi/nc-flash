/* Ghidra analysis output; verify against original SH instructions. */

/* StockBACA8~0.85 isoutsidezero tolerance;6D00=RTZ(8248/BACA8). Couplesnormalangle255C8
   toabsoluteoverride source;cross-task timingopen. */

uint Control_PublishNormalOffset(void)

{
  uint uVar1;
  float extraout_fr0;
  
  uVar1 = (*(code *)PTR_FUN_00039e14)
                    (*(undefined4 *)PTR_ThrottleCandidate_AngleMultiplier_00039e10,0,DAT_00039e0c);
  if ((uVar1 & 0xff) != 0) {
    uVar1 = (*(code *)PTR_FUN_00039e1c)(PTR_Control_BoundedOverrideSource_00039e18);
    *(float *)PTR_Control_NormalCommandOffset_00039e30 =
         extraout_fr0 / *(float *)PTR_ThrottleCandidate_AngleMultiplier_00039e10;
  }
  return uVar1;
}

