/* Ghidra analysis output; verify against original SH instructions. */

/* Stockdescriptor setsbit14 ifflag&1==0 elseclears; original5B25C executes. Unrelatedbitsretain.
   See tcu-output-pin-switch.txt. */

uint PortOutput_SelectBitValue(uint param_1,undefined4 param_2,char param_3,char param_4)

{
  uint uVar1;
  
  if ((bool)param_3 == (param_4 != '\0')) {
    uVar1 = (*(code *)PTR_FUN_0001427c)();
    param_1 = param_1 | uVar1;
  }
  else {
    uVar1 = (*(code *)PTR_FUN_0001427c)();
    param_1 = param_1 & ~uVar1;
  }
  return param_1;
}

