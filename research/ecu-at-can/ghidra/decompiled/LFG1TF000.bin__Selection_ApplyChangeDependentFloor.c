/* Ghidra analysis output; verify against original SH instructions. */

/* Stock77334/77336 zero: negative92B8 AND92D5mask20 AND8080!=FF admits floor9B3C to*r4 andFF to*r5
   if request below floor. Flag set resets82C5.108 isolated and720 complete pipeline cases;21734
   clears enablingmask20. Injected activation is not normal-operation proof. See
   selection-pipeline.txt. */

void Selection_ApplyChangeDependentFloor(byte *param_1,undefined1 *param_2)

{
  byte bVar1;
  bool bVar2;
  bool bVar3;
  
  bVar1 = *PTR_Selection_PreviousIndex_00046dc0;
  bVar2 = (*PTR_ApplicationFaultFlags92D5_00046dc4 & 0x20) != 0;
  bVar3 = false;
  if (bVar2) {
    *PTR_DAT_00046dc8 = 0;
  }
  if ((*(short *)PTR_CAN201_Byte6HistoryChange_00046dcc < *(short *)PTR_DAT_00046dd0) &&
     (((bVar2 || ((byte)*PTR_DAT_00046dc8 < (byte)*PTR_DAT_00046dd4)) &&
      (TransmissionStateClass != 0xff)))) {
    bVar3 = true;
  }
  if ((bVar3) && (*param_1 < bVar1)) {
    *param_1 = bVar1;
    *param_2 = (char)DAT_00046dba;
  }
  return;
}

