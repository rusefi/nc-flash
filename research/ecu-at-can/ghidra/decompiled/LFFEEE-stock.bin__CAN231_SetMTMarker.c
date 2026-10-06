/* Ghidra analysis output; verify against original SH instructions. */

/* While mode40 set writes6AC6=FF; otherwise retains it. Published as CAN231byte0 under independent
   pack gate. */

int CAN231_SetMTMarker(void)

{
  int iVar1;
  
  iVar1 = -(((*PTR_TransmissionModeFlags_00035cb8 & 0x40) == 0) - 1);
  if (iVar1 == 1) {
    *PTR_DAT_00035cbc = (char)DAT_00035cb6;
  }
  return iVar1;
}

