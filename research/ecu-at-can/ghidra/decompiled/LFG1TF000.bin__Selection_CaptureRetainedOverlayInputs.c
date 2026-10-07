/* Ghidra analysis output; verify against original SH instructions. */

/* Captures9336->9BF6,9390->9BF8;92C9bits0/1 independently substitute ROM77320/22 (both10240). Runs
   after46580 inside46200, so new values affect next-call hysteresis.150 direct cases. */

void Selection_CaptureRetainedOverlayInputs(void)

{
  undefined2 uVar1;
  undefined2 uVar2;
  
  uVar1 = *(undefined2 *)PTR_DAT_00046490;
  uVar2 = *(undefined2 *)PTR_DAT_00046494;
  if ((PTR_DAT_00046498[1] & 1) == 1) {
    uVar1 = *(undefined2 *)PTR_Selection_OverlayHysteresisCalibration_6__0004649c;
  }
  if ((PTR_DAT_00046498[1] & 2) != 0) {
    uVar2 = *(undefined2 *)PTR_Selection_OverlayHysteresisCalibration_7__000464a0;
  }
  *(undefined2 *)(int)DAT_0004648a = uVar1;
  *(undefined2 *)(int)DAT_0004648c = uVar2;
  return;
}

