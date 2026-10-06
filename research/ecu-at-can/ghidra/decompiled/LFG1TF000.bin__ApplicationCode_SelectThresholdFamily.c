/* Ghidra analysis output; verify against original SH instructions. */

/* Codes0..4 and5..9 map0..4;10->5;others->6. Executed with allbytecodes through3138A. See
   tcu-request-dispatch.txt. */

undefined4 ApplicationCode_SelectThresholdFamily(short param_1)

{
  undefined4 uVar1;
  
  if (param_1 == 0) {
LAB_000316e0:
    uVar1 = 0;
  }
  else {
    if (param_1 == 1) {
      return 1;
    }
    if (param_1 == 2) {
      return 2;
    }
    if (param_1 == 3) {
      return 3;
    }
    if (param_1 != 4) {
      if (param_1 == 5) goto LAB_000316e0;
      if (param_1 == 6) {
        return 1;
      }
      if (param_1 == 7) {
        return 2;
      }
      if (param_1 == 8) {
        return 3;
      }
      if (param_1 != 9) {
        if (param_1 == 10) {
          return 5;
        }
        return 6;
      }
    }
    uVar1 = 4;
  }
  return uVar1;
}

