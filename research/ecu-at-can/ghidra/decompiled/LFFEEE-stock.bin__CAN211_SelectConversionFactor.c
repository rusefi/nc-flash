/* Ghidra analysis output; verify against original SH instructions. */

/* Writes protected7154. Bit40clear multiplies6A38*6A3C; MT chooses ratio table/fallback716C.64
   synthetic cases verified; factor provenance remains open. */

void CAN211_SelectConversionFactor(void)

{
  char cVar1;
  float *pfVar2;
  float fVar3;
  
  cVar1 = *PTR_DAT_0003f694;
  if ((*PTR_TransmissionModeFlags_0003f698 & 0x40) == 0) {
    fVar3 = *(float *)PTR_DAT_0003f6a0 * *(float *)PTR_DAT_0003f69c;
    goto LAB_0003f6d4;
  }
  pfVar2 = (float *)PTR_DAT_0003f6ac;
  if ((*PTR_DAT_0003f6a4 != '\0') && (*PTR_DAT_0003f6a8 != '\x01')) {
    pfVar2 = (float *)PTR_DAT_0003f6b0;
    if (cVar1 == '\x01') {
LAB_0003f674:
      fVar3 = *pfVar2;
      goto LAB_0003f6d4;
    }
    pfVar2 = (float *)PTR_DAT_0003f6b4;
    if (cVar1 != '\x02') {
      pfVar2 = (float *)PTR_DAT_0003f6b8;
      if (cVar1 == '\x03') goto LAB_0003f674;
      pfVar2 = (float *)PTR_DAT_0003f6bc;
      if (cVar1 != '\x04') {
        pfVar2 = (float *)PTR_DAT_0003f6c0;
        if (cVar1 == '\x05') goto LAB_0003f674;
        pfVar2 = (float *)PTR_DAT_0003f8d4;
        if (cVar1 != '\x06') {
          fVar3 = *(float *)PTR_DAT_0003f8d8;
          goto LAB_0003f6d4;
        }
      }
    }
  }
  fVar3 = *pfVar2;
LAB_0003f6d4:
  (*(code *)PTR_FUN_0003f8e0)(fVar3,PTR_CAN211_ConversionFactor_0003f8dc);
  return;
}

