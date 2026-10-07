/* Ghidra analysis output; verify against original SH instructions. */

/* Returns1 onlyif92C9bit6/9317bit0/92C6bit1 clear.160 actualnative return24FD4 unchangedwholeRAM
   checks: admittedthrough44, inhibited46..288, readmitted290; separate24FA0 timerpolicy
   stillforcescut0. tcu-recovery-cut.txt. */

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

