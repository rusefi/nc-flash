/* Ghidra analysis output; verify against original SH instructions. */

/* Reads B8296 unless FF; FF takes configuration fallback. */

uint Config_ReadTransmissionSelector(void)

{
  undefined *puVar1;
  uint uVar2;
  
  puVar1 = PTR_DAT_00042a5c;
  uVar2 = (uint)(char)*PTR_TransmissionSelector_00042a60;
  if ((byte)*PTR_TransmissionSelector_00042a60 == DAT_00042a5a) {
    uVar2 = 0;
    do {
      if (*PTR_DAT_00042a68 == PTR_DAT_00042a64[uVar2 & 0xff]) break;
      uVar2 = uVar2 + 1;
    } while ((uVar2 & 0xff) < 3);
    if ((uVar2 & 0xff) < 3) {
      *PTR_DAT_00042a5c = 0;
      if ((uVar2 & 0xff) == 2) {
        uVar2 = uVar2 + 1;
      }
    }
    else {
      *PTR_DAT_00042a5c = 1;
    }
  }
  else {
    *PTR_DAT_00042a5c = 0;
  }
  if (*puVar1 == '\x01') {
    if (*PTR_DAT_00042a6c == '\0') {
      uVar2 = 1;
    }
    else {
      uVar2 = 0;
    }
  }
  return uVar2;
}

