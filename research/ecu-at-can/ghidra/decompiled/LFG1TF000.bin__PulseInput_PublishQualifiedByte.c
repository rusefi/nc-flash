/* Ghidra analysis output; verify against original SH instructions. */

/* Executed:88CD==2+A991bit0 copies88CC/status1; elsemask4 stock0/status4; elsemask2 hold/status3;
   elsehold/status2. Complete phase0/4 task calls23DD0 BEFORE this publisher. */

void PulseInput_PublishQualifiedByte(void)

{
  undefined1 uVar1;
  undefined1 uVar2;
  byte local_10 [8];
  
  uVar2 = 2;
  uVar1 = *PTR_PulseInput_PublishedByte_0005138c;
  (*(code *)PTR_FUN_00051398)(local_10,PTR_DAT_00051394,1);
  if ((*PTR_PulseInput_RawStatus_0005139c == '\x02') && ((local_10[0] & 1) == 1)) {
    uVar1 = *PTR_PulseInput_RawBit_000513a0;
    uVar2 = 1;
  }
  else if ((local_10[0] & 4) == 0) {
    if ((local_10[0] & 2) != 0) {
      uVar2 = 3;
    }
  }
  else {
    uVar1 = *PTR_DAT_000513a4;
    uVar2 = 4;
  }
  *PTR_PulseInput_PublishedByte_0005138c = uVar1;
  *PTR_PulseInput_PublicationStatus_00051390 = uVar2;
  return;
}

