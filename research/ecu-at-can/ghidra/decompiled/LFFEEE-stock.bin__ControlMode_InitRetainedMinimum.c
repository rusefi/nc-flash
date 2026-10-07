/* Ghidra analysis output; verify against original SH instructions. */

/* Bitcopy67D0->67D8. Originalcallerload16A76/call16A78 static; functionexecuted in10directcases
   andinitialization. Notfullstartup. */

void ControlMode_InitRetainedMinimum(void)

{
  *(undefined4 *)PTR_ControlMode_RetainedMinimum_00030614 =
       *(undefined4 *)PTR_ControlMode_BiasedInput_00030600;
  return;
}

