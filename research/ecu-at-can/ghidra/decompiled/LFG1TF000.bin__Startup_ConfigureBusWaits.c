/* Ghidra analysis output; verify against original SH instructions. */

/* 256 original wholeRAM/register/MMIO cases writeWCR EC24=3333 fromexplicitinitial0/7777/FFFF/3333.
   Manualtable176 vssection184 resetconflict retained; no guessed reset/bustiming.
   tcu-basic-hardware-startup.txt. */

void Startup_ConfigureBusWaits(void)

{
  *(undefined2 *)(int)DAT_00014524 = DAT_00014522;
  return;
}

