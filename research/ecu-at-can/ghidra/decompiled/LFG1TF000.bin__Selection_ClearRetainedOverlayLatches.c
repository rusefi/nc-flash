/* Ghidra analysis output; verify against original SH instructions. */

/* Clears only low3 bits of9BF5 and9BF4. Does not clear hysteresisbit3,9AEA bit2,source9B40 or
   descriptor arrays. Earlier primary producer rebuild handles descriptor withdrawal in4530C. */

void Selection_ClearRetainedOverlayLatches(void)

{
  undefined *puVar1;
  byte *pbVar2;
  
  pbVar2 = (byte *)(int)DAT_00046570;
  *pbVar2 = *pbVar2 & 0xfb;
  *pbVar2 = *pbVar2 & 0xfd;
  *pbVar2 = *pbVar2 & 0xfe;
  puVar1 = PTR_Selection_OverlayAppliedFlags_0004657c;
  *PTR_Selection_OverlayAppliedFlags_0004657c = *PTR_Selection_OverlayAppliedFlags_0004657c & 0xfb;
  *puVar1 = *puVar1 & 0xfd;
  *puVar1 = *puVar1 & 0xfe;
  return;
}

