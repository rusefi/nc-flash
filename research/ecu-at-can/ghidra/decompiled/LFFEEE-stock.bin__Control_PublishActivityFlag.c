/* Ghidra analysis output; verify against original SH instructions. */

/* Executed20736 cases:735B boolean of735Abits5/6,735Cexact1,or735Abit7 withany82A8/A433/9149exact1.
   Physicalroles unproved. */

uint Control_PublishActivityFlag(void)

{
  uint uVar1;
  
  uVar1 = 1;
  if (((((*PTR_DAT_00042c50 & 0x40) == 0) && (uVar1 = 1, (*PTR_DAT_00042c50 & 0x20) == 0)) &&
      (uVar1 = 1, *PTR_Control_ModeHoldFlag_00042c58 != '\x01')) &&
     ((uVar1 = -((((int)(char)*PTR_DAT_00042c50 & 0x80U) == 0) - 1), uVar1 != 1 ||
      (((uVar1 = 1, *PTR_DAT_00042c5c != '\x01' && (uVar1 = 1, *PTR_DAT_00042c60 != '\x01')) &&
       (uVar1 = (uint)(byte)*PTR_Control_ActivityHold_00042c64, uVar1 != 1)))))) {
    *DAT_00042c54 = 0;
  }
  else {
    *DAT_00042c54 = 1;
  }
  return uVar1;
}

