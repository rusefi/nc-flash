/* Ghidra analysis output; verify against original SH instructions. */

/* Writes693C=bool(695B&0x1E);256arbitrarymaskcases. Original seven-call1876E..18798 slice verified
   incontrol-mode-followers.txt. */

int ControlMode_PublishActiveMask(void)

{
  int iVar1;
  
  iVar1 = 1;
  if (((((*PTR_ControlMode_SelectedBit_00030cac & 0x10) == 0) &&
       (iVar1 = 1, (*PTR_ControlMode_SelectedBit_00030cac & 8) == 0)) &&
      (iVar1 = 1, (*PTR_ControlMode_SelectedBit_00030cac & 4) == 0)) &&
     (iVar1 = -(((*PTR_ControlMode_SelectedBit_00030cac & 2) == 0) - 1), iVar1 != 1)) {
    *PTR_ControlMode_ActiveMaskFlag_00030ca8 = 0;
  }
  else {
    *PTR_ControlMode_ActiveMaskFlag_00030ca8 = 1;
  }
  return iVar1;
}

