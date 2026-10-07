/* Ghidra analysis output; verify against original SH instructions. */

/* Onlyoddentry6CBC copies40E8->6CB4 and2508filters6CB8
   witholdweightabout0.98,epsilon.00030517578125.
   Alwaysbyteincrement/wrap.72cases/260retained/320cyclechecks. */

uint Acquisition_PublishAlternatingInput(void)

{
  undefined *puVar1;
  undefined *puVar2;
  uint uVar3;
  undefined4 extraout_fr0;
  
  puVar2 = PTR_Acquisition_AlternatingPhase_0001df80;
  puVar1 = PTR_Control_LocalFilterInput_0001df70;
  uVar3 = (uint)(byte)*PTR_Acquisition_AlternatingPhase_0001df80;
  if ((*PTR_Acquisition_AlternatingPhase_0001df80 & 1) != 0) {
    *(undefined4 *)PTR_Control_LocalFilterInput_0001df70 =
         *(undefined4 *)PTR_Acquisition_ScaledChannel1_0001df74;
    uVar3 = (*(code *)PTR_FUN_0001df8c)
                      (*(undefined4 *)puVar1,
                       *(undefined4 *)PTR_Acquisition_FilteredChannel1_0001df78,
                       1.0 - *(float *)PTR_DAT_0001df84,DAT_0001df88);
    *(undefined4 *)PTR_Acquisition_FilteredChannel1_0001df78 = extraout_fr0;
  }
  *puVar2 = *puVar2 + '\x01';
  return uVar3;
}

