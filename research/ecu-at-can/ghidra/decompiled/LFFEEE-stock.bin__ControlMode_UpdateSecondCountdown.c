/* Ghidra analysis output; verify against original SH instructions. */

/* Entry695Bbit3clear reloadsu16(6916)=DB0D4stock375;setdecrementspositiveword.30202
   mode08admissionneeds>0; leavingmodemayreloadnextcall. */

uint ControlMode_UpdateSecondCountdown(void)

{
  char cVar1;
  
  cVar1 = *PTR_ControlMode_SelectedBit_00031ca0;
  if (((int)cVar1 & 8U) == 0) {
    *DAT_00031cac = *DAT_00031cb0;
  }
  else if (*DAT_00031cac != 0) {
    *DAT_00031cac = *DAT_00031cac + (short)DAT_00031ca8;
  }
  return (int)cVar1;
}

