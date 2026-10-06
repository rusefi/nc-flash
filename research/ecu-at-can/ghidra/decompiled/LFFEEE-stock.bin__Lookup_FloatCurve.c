/* Ghidra analysis output; verify against original SH instructions. */

/* Original axis-clamped curve interpolation;71 cases acrossA2218/A2224/A2230. Other encodings
   unverified. */

float Lookup_FloatCurve(int param_1)

{
  int extraout_r3;
  float in_fr2;
  
  func_0x00002714();
  (**(code **)((int)&PTR_FUN_00002328 + (uint)*(byte *)(param_1 + 2)))();
  if (extraout_r3 != 0) {
    in_fr2 = *(float *)(param_1 + 0x10) + in_fr2 * *(float *)(param_1 + 0xc);
  }
  return in_fr2;
}

