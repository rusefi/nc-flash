/* Ghidra analysis output; verify against original SH instructions. */

/* F748=4000,F74A=8000,F74C=0,F74E=0. Compatiblemanual selectsPF14 generaloutput initially0;
   boardrole unknown. See tcu-output-pin-switch.txt. */

void OutputPins_InitPortF(void)

{
  undefined2 *puVar1;
  
  puVar1 = (undefined2 *)(int)DAT_000148aa;
  *puVar1 = DAT_000148a8;
  *(short *)(int)DAT_000148ac = (short)PTR_DAT_000148c8;
  *(undefined2 *)(int)DAT_000148ae = 0;
  puVar1[3] = 0;
  return;
}

