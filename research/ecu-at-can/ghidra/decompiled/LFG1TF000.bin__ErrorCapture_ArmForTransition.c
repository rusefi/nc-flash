/* Ghidra analysis output; verify against original SH instructions. */

/* Nonzero95C2 and code3/4/8/9/11 arm state2; index3 for3/8/11,index4 for4/9; captures30C20 into95C0
   and80D8.1032 enabled/disabled/code cases verified. */

void ErrorCapture_ArmForTransition(short param_1)

{
  char *pcVar1;
  undefined1 uVar2;
  
  pcVar1 = (char *)(int)DAT_00030c0a;
  if ((*pcVar1 != '\0') &&
     ((((param_1 == 3 || (param_1 == 8)) || (param_1 == 4)) || ((param_1 == 9 || (param_1 == 0xb))))
     )) {
    *(short *)(int)DAT_00030c0c = param_1;
    *pcVar1 = '\x02';
    uVar2 = 4;
    if ((param_1 == 3) || ((param_1 == 8 || (param_1 == 0xb)))) {
      uVar2 = 3;
    }
    *(undefined1 *)(int)DAT_00030c0e = uVar2;
    Request_Code9HoldSource = ErrorCapture_ClippedDifference();
    *(undefined2 *)(int)DAT_00030c10 = Request_Code9HoldSource;
  }
  return;
}

