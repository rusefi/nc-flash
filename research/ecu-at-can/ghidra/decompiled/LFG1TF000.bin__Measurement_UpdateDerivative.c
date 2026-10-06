/* Ghidra analysis output; verify against original SH instructions. */

/* Signedword
   delta=floor((old923E-old9240-old9242+9234)/4)->80F0;clamp(trunc(delta*6103/256),-32768,32767)->923C;
   shifts3 history words.625 boundary cases/MACL preservation. See tcu-measurement.txt. */

void Measurement_UpdateDerivative(void)

{
  short sVar1;
  int iVar2;
  int iVar3;
  short *psVar4;
  int iVar5;
  
  psVar4 = (short *)(int)DAT_000214c6;
  sVar1 = *(short *)PTR_Measurement_SelectedInternalSample_000214d0;
  iVar3 = (((int)*psVar4 - (int)psVar4[1]) - (int)psVar4[2]) + (int)sVar1 >> 2;
  (*(code *)PTR_FUN_000214d4)();
  iVar5 = iVar3 * DAT_000214c8;
  if (iVar5 < 0) {
    iVar5 = iVar5 + DAT_000214ca;
  }
  iVar2 = iVar5 >> 8;
  if ((int)DAT_000214cc < iVar5 >> 8) {
    iVar2 = (int)DAT_000214cc;
  }
  if (iVar2 < DAT_000214ce) {
    iVar2 = (int)DAT_000214ce;
  }
  Measurement_DerivativeForRequest = (undefined2)iVar3;
  *(short *)PTR_DAT_000214d8 = (short)iVar2;
  psVar4[2] = psVar4[1];
  psVar4[1] = *psVar4;
  *psVar4 = sVar1;
  return;
}

