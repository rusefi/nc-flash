/* Ghidra analysis output; verify against original SH instructions. */

/* u16[80B6]>0 andA963bit0 andu16[8900]<12.48 recovery boundary/gate cases; physical units
   unresolved. */

undefined4 SpeedFault_CheckRecovery(void)

{
  undefined4 uVar1;
  
  uVar1 = 0;
  if (((DAT_ffff80b6 != 0) && ((*PTR_DAT_00058c7c & 1) == 1)) &&
     (*(ushort *)PTR_SpeedFault_OtherCaptureCount_00058c80 < 0xc)) {
    uVar1 = 1;
  }
  return uVar1;
}

