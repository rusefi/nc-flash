/* Ghidra analysis output; verify against original SH instructions. */

/* Returns1 only when92C9bit6,9317bit0,92C6bit1 clear.24FA0 clears9454 when not admitted. */

undefined4 CAN216_AdmitCylinderCutRequest(void)

{
  undefined4 uVar1;
  
  uVar1 = 0;
  if ((((*PTR_ApplicationFaultFlags92C9_00025178 & 0x40) == 0) && ((*PTR_DAT_00025170 & 1) == 0)) &&
     ((*PTR_ApplicationFaultFlags92C6_0002517c & 2) == 0)) {
    uVar1 = 1;
  }
  return uVar1;
}

