/* Ghidra analysis output; verify against original SH instructions. */

/* Only mode40 writes6AC4=FFFF; packed big-endian into231bytes2/3. No update otherwise. */

int CAN231_SetMTWordMarker(void)

{
  int iVar1;
  
  iVar1 = -(((*PTR_TransmissionModeFlags_00035cb8 & 0x40) == 0) - 1);
  if (iVar1 == 1) {
    *(short *)PTR_DAT_00035cdc = (short)DAT_00035cd8;
  }
  return iVar1;
}

