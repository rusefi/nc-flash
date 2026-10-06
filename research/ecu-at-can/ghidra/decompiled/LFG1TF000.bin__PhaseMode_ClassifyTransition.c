/* Ghidra analysis output; verify against original SH instructions. */

/* Low16 argument0..4 returns1,5..11 returns2,other returns0.19 boundary cases; tcu-phase-mode.txt.
    */

undefined4 PhaseMode_ClassifyTransition(short param_1)

{
  undefined4 uVar1;
  
  uVar1 = 0;
  if ((((param_1 == 0) || (param_1 == 1)) || (param_1 == 2)) || ((param_1 == 3 || (param_1 == 4))))
  {
    uVar1 = 1;
  }
  if ((((param_1 == 5) || (param_1 == 6)) ||
      ((param_1 == 7 || (((param_1 == 8 || (param_1 == 9)) || (param_1 == 10)))))) ||
     (param_1 == 0xb)) {
    uVar1 = 2;
  }
  return uVar1;
}

