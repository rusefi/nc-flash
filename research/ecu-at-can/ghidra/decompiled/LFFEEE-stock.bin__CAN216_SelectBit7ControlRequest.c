/* Ghidra analysis output; verify against original SH instructions. */

/* 6E57=1 iff B81B2==0 and6A5F nonzero; stockB81B2=1 forces0.1024 paired TCU216/ECU/CAN211 latch
   cases verified. */

void CAN216_SelectBit7ControlRequest(void)

{
  if ((*PTR_CAN216_Bit7ControlDisable_0003b650 == '\0') && (*PTR_DAT_0003b654 != '\0')) {
    *PTR_CAN216_Bit7ControlRequest_0003b64c = 1;
  }
  else {
    *PTR_CAN216_Bit7ControlRequest_0003b64c = 0;
  }
  return;
}

