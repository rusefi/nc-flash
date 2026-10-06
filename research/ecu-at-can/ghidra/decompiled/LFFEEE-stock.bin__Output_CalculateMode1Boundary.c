/* Ghidra analysis output; verify against original SH instructions. */

/* Signed Q16 division2138 of41E4+child+8+trunc(CC1E4/0.25) by410C;*180+child+12 with32-bit wrap.
   Physical timing units unproved. */

int Output_CalculateMode1Boundary(char *param_1)

{
  int iVar1;
  int iVar2;
  
  iVar1 = (*pcRam000205c8)((int)*param_1);
  iVar2 = (*pcRam000205cc)((int)*param_1);
  iVar1 = (*pcRam000205d4)(iVar2 + *(int *)(param_1 + 8) + iVar1,*puRam000205d0);
  return iVar1 * sRam000205c4 + *(int *)(param_1 + 0xc);
}

