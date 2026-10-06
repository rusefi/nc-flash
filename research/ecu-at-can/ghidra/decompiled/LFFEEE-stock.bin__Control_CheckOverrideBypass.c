/* Ghidra analysis output; verify against original SH instructions. */

/* Stock bypass usesOLD566E,93C3/92CB/932A,722A/5664,5633 and6642/43/protected213A.
   Fullcallerretainedhistory tested;not numericoutputdisable. */

undefined4 Control_CheckOverrideBypass(char param_1,ushort param_2,char param_3)

{
  char cVar1;
  undefined4 uVar2;
  
  cVar1 = (*(code *)PTR_FUN_00025348)(PTR_Control_FeedbackOverrideEnabled_00025344);
  if (((((cVar1 == '\0') && (param_3 == '\0')) &&
       ((*PTR_DAT_0002534c == '\x01' || (*PTR_DAT_00025350 == '\x01')))) ||
      (((param_1 == '\0' && (*(ushort *)PTR_DAT_00025354 < param_2)) ||
       (*PTR_DAT_00025358 == '\x01')))) ||
     (((*PTR_DAT_0002535c == '\0' && (*PTR_DAT_00025360 == '\0')) &&
      (cVar1 = (*(code *)PTR_Protected_ReadByteOrDefault_00025368)(PTR_DAT_00025364,0),
      cVar1 == '\0')))) {
    uVar2 = 1;
  }
  else {
    uVar2 = 0;
  }
  return uVar2;
}

