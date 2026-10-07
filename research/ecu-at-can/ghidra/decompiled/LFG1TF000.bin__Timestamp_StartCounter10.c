/* Ghidra analysis output; verify against original SH instructions. */

/* 256 original exact2MMIO cases PASS:F401byte read thenold|80 write,unchangedRAM/callee
   registers/SR. CompatibleSH7055S STR10. PSCR4=1 conditionalPphi/2; resetwordwidth/sourceconflict
   remains. tcu-timestamp-configuration.txt. */

void Timestamp_StartCounter10(void)

{
  *(byte *)(int)DAT_00015572 = *(byte *)(int)DAT_00015572 | 0x80;
  return;
}

