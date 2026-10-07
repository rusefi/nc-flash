/* Ghidra analysis output; verify against original SH instructions. */

/* Original2098 zeroextends6CAC andscales byfloat30604=0.08320312201976776 ->67D4.
   All256byteschecked; highinputsetsdownstream6937. Upstreamrecordnotyetexecuted. */

void ControlMode_ScaleByteInput(void)

{
  undefined4 uVar1;
  
  uVar1 = (*(code *)PTR_FUN_0003060c)
                    (DAT_00030604,0,(int)(char)*PTR_Acquisition_Channel8HighByte_00030608);
  *(undefined4 *)PTR_ControlMode_ScaledByteInput_00030610 = uVar1;
  return;
}

