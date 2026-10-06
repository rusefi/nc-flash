/* Ghidra analysis output; verify against original SH instructions. */

/* FR4>=FR5 sets1;FR4<FR5-FR6 clears0;otherwise hold inputR4. Executed in complete request
   classifier. */

undefined4 Pattern_Hysteresis(float param_1,float param_2,float param_3,undefined4 param_4)

{
  if (param_1 < param_2) {
    if (param_1 < param_2 - param_3) {
      param_4 = 0;
    }
  }
  else {
    param_4 = 1;
  }
  return param_4;
}

