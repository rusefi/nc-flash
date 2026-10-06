/* Ghidra analysis output; verify against original SH instructions. */

/* Fresh88E8 if88EA==2 andA98Cbit0; elsebit2 substitute9240/status4, elsebit1
   substitute9240/status3, else hold/status2. Clamp selected value -1000..9240. */

int CAN215_SelectBaseInput(void)

{
  char cVar1;
  int iVar2;
  undefined1 uVar3;
  byte local_8 [8];
  
  cVar1 = *PTR_CAN215_DifferenceValidity_00051788;
  (*(code *)PTR_FUN_00051790)(local_8,PTR_CAN215_BaseDiagnosticSummary_0005178c,1);
  iVar2 = (int)SparkRequest_BaseInput;
  uVar3 = 2;
  if ((cVar1 == '\x02') && ((local_8[0] & 1) == 1)) {
    iVar2 = (int)*(short *)PTR_CAN215_ConvertedDifference_00051794;
    uVar3 = 1;
  }
  else if ((local_8[0] & 4) == 0) {
    if ((local_8[0] & 2) != 0) {
      iVar2 = (int)*(short *)PTR_DAT_00051798;
      uVar3 = 3;
    }
  }
  else {
    iVar2 = (int)*(short *)PTR_DAT_00051798;
    uVar3 = 4;
  }
  if (*(short *)PTR_DAT_0005179c < (short)iVar2) {
    iVar2 = (int)*(short *)PTR_DAT_0005179c;
  }
  else if ((short)iVar2 < *(short *)PTR_DAT_000517a0) {
    iVar2 = (int)*(short *)PTR_DAT_000517a0;
  }
  SparkRequest_BaseInput = (short)iVar2;
  *PTR_CAN215_BaseSelectionStatus_00051784 = uVar3;
  return iVar2;
}

