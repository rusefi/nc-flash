/* Ghidra analysis output; verify against original SH instructions. */

/* Original descriptor dispatch/axis search/bilinear float interpolation.5508 node/midpoint/bounds
   cases across13 stock maps; tested encoding0. MACH/MACL restored. */

float Lookup_FloatMap2D(int param_1)

{
  int iVar1;
  float in_fr2;
  
  FUN_00002748();
  iVar1 = (int)*(char *)(param_1 + 0x10);
  (**(code **)((int)&PTR_LAB_0000239c + iVar1))();
  if (iVar1 != 0) {
    in_fr2 = *(float *)(param_1 + 0x18) + in_fr2 * *(float *)(param_1 + 0x14);
  }
  return in_fr2;
}

