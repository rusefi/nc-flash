/* Ghidra analysis output; verify against original SH instructions. */

/* With GBR+80==6, source0..5 -> wire1..6; invalid-state cases0/E/F. */

undefined4 CAN231_EncodeSixState(char param_1)

{
  undefined4 uVar1;
  
  uVar1 = 0xf;
  if ((*PTR_DAT_00019954 & 0x40) == 0) {
    if (TransmissionStateClass == 6) {
      if (param_1 == '\0') {
        uVar1 = 1;
      }
      else if (param_1 == '\x01') {
        uVar1 = 2;
      }
      else if (param_1 == '\x02') {
        uVar1 = 3;
      }
      else if (param_1 == '\x03') {
        uVar1 = 4;
      }
      else if (param_1 == '\x04') {
        uVar1 = 5;
      }
      else if (param_1 == '\x05') {
        uVar1 = 6;
      }
    }
    else if (TransmissionStateClass == 0xff) {
      uVar1 = 0xe;
      if ((*PTR_DAT_000199a8 & 1) == 1) {
        uVar1 = 0;
      }
    }
    else if (TransmissionStateClass == 0) {
      uVar1 = 0;
    }
  }
  return uVar1;
}

