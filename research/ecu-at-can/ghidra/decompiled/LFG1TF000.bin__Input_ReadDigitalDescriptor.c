/* Ghidra analysis output; verify against original SH instructions. */

/* Reads descriptor pointer, bit and polarity; calls1432C and returns Boolean. Peripheral reads use
   explicit test samples only. */

bool Input_ReadDigitalDescriptor(int *param_1)

{
  char cVar1;
  
  cVar1 = '\0';
  if ((param_1 != (int *)0x0) && (*param_1 != 0)) {
    cVar1 = Input_CompareSampledBit
                      (*param_1,(int)*(char *)(param_1 + 1),*(undefined1 *)((int)param_1 + 5));
  }
  return cVar1 != '\0';
}

