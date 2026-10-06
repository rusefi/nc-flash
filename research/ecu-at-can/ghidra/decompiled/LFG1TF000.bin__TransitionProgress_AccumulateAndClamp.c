/* Ghidra analysis output; verify against original SH instructions. */

/* Signedwrapped32 sumr5+r6,clamp0..25600;lowbyte r4exact1
   insteadcapsatstock770C4=3840.378boundarycasesincloverflow; tcu-transition-progress.txt. */

int TransitionProgress_AccumulateAndClamp(char param_1,int param_2,int param_3)

{
  short sVar1;
  int iVar2;
  
  sVar1 = DAT_00032c4e;
  if (param_1 == '\x01') {
    sVar1 = *(short *)PTR_TransitionProgress_ReducedCap_00032c80;
  }
  iVar2 = param_2 + param_3;
  if ((int)sVar1 < param_2 + param_3) {
    iVar2 = (int)sVar1;
  }
  if (iVar2 < 0) {
    iVar2 = 0;
  }
  return iVar2;
}

