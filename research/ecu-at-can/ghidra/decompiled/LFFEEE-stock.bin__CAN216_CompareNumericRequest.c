/* Ghidra analysis output; verify against original SH instructions. */

/* 6E3A=1 iff MTbit734A40clear AND71C0>6E04; else0.40 original-code cases cover strict
   comparison/mode. */

int CAN216_CompareNumericRequest(void)

{
  int iVar1;
  
  iVar1 = -(((*PTR_TransmissionModeFlags_0003b018 & 0x40) == 0) - 1);
  if (iVar1 == 1) {
    *PTR_CAN216_NumericRequestActive_0003b020 = 0;
  }
  else if (*(float *)PTR_Model_NetBaselineValue_0003b024 <=
           *(float *)PTR_CAN216_SelectedNumericRequest_0003b028) {
    *PTR_CAN216_NumericRequestActive_0003b020 = 0;
  }
  else {
    iVar1 = 1;
    *PTR_CAN216_NumericRequestActive_0003b020 = 1;
  }
  return iVar1;
}

