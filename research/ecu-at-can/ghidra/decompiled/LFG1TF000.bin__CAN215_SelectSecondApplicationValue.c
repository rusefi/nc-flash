/* Ghidra analysis output; verify against original SH instructions. */

/* Fresh88EC if88EE2 andA98Cbit0; otherwisebit2/bit1 ->9240/status4/3, elsehold/status2. Clamp
   -1000..9240.4096 policy/scaling cases; sharedgroup3B affects both fields. */

int CAN215_SelectSecondApplicationValue(void)

{
  char cVar1;
  int iVar2;
  undefined1 uVar3;
  byte local_8 [8];
  
  cVar1 = *PTR_CAN215_SecondDifferenceValidity_00051854;
  (*(code *)PTR_FUN_0005185c)(local_8,PTR_CAN215_BaseDiagnosticSummary_00051858,1);
  iVar2 = (int)CAN215_SecondApplicationValue;
  uVar3 = 2;
  if ((cVar1 == '\x02') && ((local_8[0] & 1) == 1)) {
    iVar2 = (int)*(short *)PTR_CAN215_ConvertedSecondDifference_00051860;
    uVar3 = 1;
  }
  else if ((local_8[0] & 4) == 0) {
    if ((local_8[0] & 2) != 0) {
      iVar2 = (int)*(short *)PTR_DAT_00051864;
      uVar3 = 3;
    }
  }
  else {
    iVar2 = (int)*(short *)PTR_DAT_00051864;
    uVar3 = 4;
  }
  if (*(short *)PTR_DAT_00051868 < (short)iVar2) {
    iVar2 = (int)*(short *)PTR_DAT_00051868;
  }
  else if ((short)iVar2 < *(short *)PTR_DAT_0005186c) {
    iVar2 = (int)*(short *)PTR_DAT_0005186c;
  }
  CAN215_SecondApplicationValue = (short)iVar2;
  *PTR_CAN215_SecondSelectionStatus_00051850 = uVar3;
  return iVar2;
}

