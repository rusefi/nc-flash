/* Ghidra analysis output; verify against original SH instructions. */

/* Protected723E=(44A4 bit6 clear OR protected7002==1). Source byte and nonboolean override cases
   executed; physical switch name unproved. */

void Input_UpdateLocalBit6Flag(void)

{
  char cVar1;
  undefined4 uVar2;
  
  if (((*PTR_Input_FilteredSerialBankOne_00041368 & 0x40) == 0) ||
     (cVar1 = (*(code *)PTR_FUN_0004134c)(PTR_DAT_00041354), cVar1 == '\x01')) {
    uVar2 = 1;
  }
  else {
    uVar2 = 0;
  }
  (*(code *)PTR_FUN_00041350)(PTR_DAT_00041374,uVar2);
  return;
}

