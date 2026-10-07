/* Ghidra analysis output; verify against original SH instructions. */

/* Nominal400..500inputratio, stocklower/upperboth1 =>6848=6844.28finitecases
   andcaller/retainedcoverage. Nonstock calibration nottested. */

uint ControlSecondary_ScaleExtrapolation(void)

{
  undefined *puVar1;
  uint uVar2;
  float fVar3;
  float extraout_fr0;
  
  puVar1 = PTR_DAT_00031b5c;
  uVar2 = (*(code *)PTR_FUN_00031b68)
                    (*(undefined4 *)PTR_DAT_00031b64,*(undefined4 *)PTR_DAT_00031b5c,DAT_00031b60);
  if ((uVar2 & 0xff) != 0) {
    fVar3 = (float)(*(code *)PTR_FUN_00031b70)(PTR_DAT_00031b6c);
    uVar2 = (*(code *)PTR_FUN_00031b78)
                      ((fVar3 - *(float *)puVar1) / (*(float *)PTR_DAT_00031b64 - *(float *)puVar1),
                       *(undefined4 *)PTR_DAT_00031b74,0x3f800000);
    *(float *)PTR_ControlSecondary_ScaledTarget_00031b80 =
         *(float *)PTR_ControlSecondary_ExtrapolatedTarget_00031b7c * extraout_fr0;
  }
  return uVar2;
}

