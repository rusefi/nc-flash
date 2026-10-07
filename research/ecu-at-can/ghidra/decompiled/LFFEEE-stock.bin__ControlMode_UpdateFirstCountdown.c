/* Ghidra analysis output; verify against original SH instructions. */

/* Entry695Bbit4clear reloadsu16(6914)=DB0D2stock38;setdecrementspositiveword. Original1C9B4
   source->31BE6->31C0Esegmentverified. Callsnotmilliseconds. */

uint ControlMode_UpdateFirstCountdown(void)

{
  char cVar1;
  
  cVar1 = *PTR_ControlMode_SelectedBit_00031ca0;
  if (((int)cVar1 & 0x10U) == 0) {
    *DAT_00031c9c = *(short *)PTR_DAT_00031ca4;
  }
  else if (*DAT_00031c9c != 0) {
    *DAT_00031c9c = *DAT_00031c9c + (short)DAT_00031ca8;
  }
  return (int)cVar1;
}

