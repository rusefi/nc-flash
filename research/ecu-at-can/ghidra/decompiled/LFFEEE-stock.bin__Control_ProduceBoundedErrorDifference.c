/* Ghidra analysis output; verify against original SH instructions. */

/* 6804=clamp(R(6800-old6970),-2.5,2.5), then6970=6800. Original retained difference executed. */

void Control_ProduceBoundedErrorDifference(void)

{
  undefined4 uVar1;
  float fVar2;
  
  fVar2 = *(float *)PTR_Control_BoundedInputError_0003147c;
  uVar1 = (*(code *)PTR_FUN_00031478)
                    (fVar2 - *(float *)PTR_Control_PreviousBoundedError_00031480,DAT_00031474,
                     DAT_00031470);
  *(undefined4 *)PTR_Control_BoundedErrorDifference_00031484 = uVar1;
  *(float *)PTR_Control_PreviousBoundedError_00031480 = fVar2;
  return;
}

