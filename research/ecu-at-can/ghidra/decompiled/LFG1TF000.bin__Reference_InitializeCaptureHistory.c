/* Ghidra analysis output; verify against original SH instructions. */

/* Initializes810D/8196/9195=FF, resets18-entry history91CC,9198/919C=FFFFFFFF. See
   tcu-reference-source.txt. */

void Reference_InitializeCaptureHistory(void)

{
  undefined1 uVar1;
  
  uVar1 = (undefined1)DAT_00020734;
  *PTR_DAT_0002073c = uVar1;
  *PTR_Reference_IdleSettlingTimer_00020740 = uVar1;
  *PTR_DAT_00020744 = uVar1;
  Reference_ResetCaptureHistory();
  *(undefined4 *)PTR_DAT_00020748 = 0xffffffff;
  *(undefined4 *)PTR_Reference_FullNormalizedPeriod_0002074c = 0xffffffff;
  return;
}

