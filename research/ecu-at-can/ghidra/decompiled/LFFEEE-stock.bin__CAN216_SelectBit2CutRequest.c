/* Ghidra analysis output; verify against original SH instructions. */

/* AT-only bit2 consumer; stock TCU sender clears this bit. */

char CAN216_SelectBit2CutRequest(void)

{
  char cVar1;
  
  if ((*PTR_TransmissionModeFlags_0003b018 & 0x40) == 0) {
    cVar1 = *PTR_DAT_0003b01c;
    if (cVar1 == '\x01') {
      *PTR_DAT_0003b014 = 1;
    }
    else {
      *PTR_DAT_0003b014 = 0;
    }
  }
  else {
    *PTR_DAT_0003b014 = 0;
    cVar1 = '\x01';
  }
  return cVar1;
}

