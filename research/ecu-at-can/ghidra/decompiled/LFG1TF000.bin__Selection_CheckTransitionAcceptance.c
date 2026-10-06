/* Ghidra analysis output; verify against original SH instructions. */

/* 9545bit2 blocksall. Otherwiseclassr5 selects484D0/487B8/48812/48860, then916Cbit0
   overridesresult1.2520 helpercases. Onsuccesswithr4!=FF stores9C64. Gate writer2D1BC is called
   by2C7B0; see transition-gate.txt. */

uint Selection_CheckTransitionAcceptance(uint param_1,char param_2)

{
  uint uVar1;
  
  uVar1 = 0;
  if ((*PTR_Transition_ControlFlags_000481f8 & 4) == 0) {
    if ((((param_2 == '\x02') || (param_2 == '\x05')) || (param_2 == '\x03')) ||
       ((param_2 == '\x04' || (param_2 == '\x1b')))) {
      uVar1 = FUN_000487b8(param_1);
    }
    else if ((param_2 == '\x10') || (param_2 == '\x11')) {
      uVar1 = FUN_00048812(param_1);
    }
    else if ((param_2 == '\x12') || (param_2 == '\x13')) {
      uVar1 = FUN_00048860(param_1);
    }
    else {
      uVar1 = FUN_000484d0(param_1);
    }
    if ((*PTR_DAT_000481fc & 1) == 1) {
      uVar1 = 1;
    }
  }
  if (((uVar1 & 0xff) == 1) && ((param_1 & 0xff) != (int)DAT_000481f2)) {
    *(char *)(int)DAT_000481f4 = (char)param_1;
  }
  return uVar1;
}

