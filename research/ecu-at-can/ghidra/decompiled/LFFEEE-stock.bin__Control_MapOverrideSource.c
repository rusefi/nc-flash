/* Ghidra analysis output; verify against original SH instructions. */

/* Stock24point A19F4 maps8014 to8250;endpoint clamping andRTZ interpolation verified. Fullbody
   control-sources.txt. */

void Control_MapOverrideSource(void)

{
  undefined4 uVar1;
  
  uVar1 = (*(code *)PTR_Lookup_FloatCurve_0005c584)
                    (*(undefined4 *)PTR_Control_SelectedOverrideInput_0005c598,
                     PTR_Control_OverrideSourceMapDescriptor_0005c59c);
  *(undefined4 *)PTR_Control_UnboundedOverrideSource_0005c5a0 = uVar1;
  return;
}

