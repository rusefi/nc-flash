/* Ghidra analysis output; verify against original SH instructions. */

/* 683C fromspecialflagcap*DB1FC(stock0),zero gate,near6808/6814cap3.75
   ormapA3A10(67DC,6808).755directcases; rawflags/equalities preserved. control-secondary-path.txt.
    */

uint ControlSecondary_SelectTarget(void)

{
  undefined *puVar1;
  char cVar3;
  uint uVar2;
  undefined4 extraout_fr0;
  float fVar4;
  undefined4 uVar5;
  
  uVar5 = *(undefined4 *)PTR_Control_BoundedInputTermSum_000319f0;
  cVar3 = (*(code *)PTR_FUN_000319fc)
                    (uVar5,*(undefined4 *)PTR_Control_AccumulatedErrorLimit_000319f8,DAT_000319f4);
  puVar1 = PTR_ControlSecondary_Target_00031a00;
  uVar2 = (uint)(byte)*PTR_DAT_00031a0c;
  if ((uVar2 == 1) && (uVar2 = (uint)(byte)*PTR_DAT_00031a10, uVar2 == 1)) {
    *(float *)PTR_ControlSecondary_Target_00031a00 =
         *(float *)(PTR_DAT_00031a08 +
                   ((int)(char)*PTR_DAT_00031a04 + (int)DAT_000319ec & 0xffU) * 4) *
         *(float *)PTR_DAT_00031a14;
  }
  else {
    if (*PTR_ControlInput_ScaleHysteresisGate_00031a18 == '\0') {
      fVar4 = 0.0;
    }
    else {
      if (cVar3 != '\0') {
        uVar2 = (*(code *)PTR_Lookup_FloatMap2D_00031a24)
                          (*(undefined4 *)PTR_ControlInput_ScaledLimitAxis_00031a1c,uVar5,
                           PTR_LAB_00031a20);
        *(undefined4 *)puVar1 = extraout_fr0;
        return uVar2;
      }
      fVar4 = *(float *)(PTR_DAT_00031a08 +
                        ((int)(char)*PTR_DAT_00031a04 + (int)DAT_000319ec & 0xffU) * 4);
    }
    *(float *)PTR_ControlSecondary_Target_00031a00 = fVar4;
  }
  return uVar2;
}

