/* Ghidra analysis output; verify against original SH instructions. */

/* Always93F4=1; operation low16 zero copies939E to93F6 and sets93F8bit0.72 direct cases; original
   phase-creation callback. */

void Qualification_CaptureOnPhaseCreation(undefined4 param_1,short param_2)

{
  byte *pbVar1;
  
  *(undefined1 *)(int)DAT_00023a2a = 1;
  if (param_2 == 0) {
    pbVar1 = (byte *)(int)DAT_00023a2c;
    *(undefined2 *)(int)DAT_00023a28 = *(undefined2 *)PTR_Qualification_ProducedLimit_00023a3c;
    *pbVar1 = *pbVar1 | 1;
  }
  return;
}

