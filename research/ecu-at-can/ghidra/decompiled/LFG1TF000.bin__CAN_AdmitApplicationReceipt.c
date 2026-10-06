/* Ghidra analysis output; verify against original SH instructions. */

/* Logical RX index<10 requires8F6C bits0C and sets8F71. Indices10/11 accepted without pending
   flag.48 cases executed. */

undefined4 CAN_AdmitApplicationReceipt(byte param_1)

{
  if (param_1 < 10) {
    if ((*PTR_DAT_0001bf6c & 0xc) == 0) {
      return 0;
    }
    *PTR_DAT_0001bf88 = 1;
  }
  return 1;
}

