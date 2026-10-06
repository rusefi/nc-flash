/* Ghidra analysis output; verify against original SH instructions. */

/* Previous8094exact1 andcurrent73B8zero reload8080 fromstockD9F11=0;elsedecrementnonzero.
   Savecurrentraw73B8to8094. */

char Control_UpdateInputHistoryHoldoff(void)

{
  char cVar1;
  undefined *puVar2;
  char cVar3;
  
  cVar3 = (*(code *)PTR_FUN_0005870c)(PTR_DAT_00058720);
  puVar2 = PTR_Control_PreviousInputHistoryStatus_00058724;
  cVar1 = *PTR_Control_PreviousInputHistoryStatus_00058724;
  if ((cVar1 == '\x01') && (cVar3 == '\0')) {
    *PTR_Control_InputHistoryHoldoff_00058728 = *PTR_DAT_0005872c;
  }
  else if (*PTR_Control_InputHistoryHoldoff_00058728 != '\0') {
    *PTR_Control_InputHistoryHoldoff_00058728 =
         *PTR_Control_InputHistoryHoldoff_00058728 + (char)DAT_000586e6;
  }
  *puVar2 = cVar3;
  return cVar1;
}

