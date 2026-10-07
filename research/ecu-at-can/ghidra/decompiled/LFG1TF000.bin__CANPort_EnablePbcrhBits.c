/* Ghidra analysis output; verify against original SH instructions. */

/* OriginalwordreadPBCRHF732,OR00A0,wordwrite.256varied16-bit inputs exactwholeRAM/register/SR/MMIO
   PASS; existingstrictConfigurationRegisters. No electricalpinproof.
   tcu-native-capture-startup.txt. */

void CANPort_EnablePbcrhBits(void)

{
  *(ushort *)(int)DAT_0001ad5e = *(ushort *)(int)DAT_0001ad5e | 0xa0;
  return;
}

