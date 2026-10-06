/* Ghidra analysis output; verify against original SH instructions. */

/* Stock C11E6 override disabled;6590 nonzero copies7181 to7182,otherwise0. */

void Pattern_ApplyRequestEnable(void)

{
  undefined1 uVar1;
  
  if (*PTR_DAT_0003feb0 == '\0') {
    if (*PTR_DAT_0003feb8 == '\0') {
      uVar1 = 0;
    }
    else {
      uVar1 = *PTR_Pattern_ClassifiedIndex_0003fe98;
    }
    *PTR_Pattern_EnabledIndex_0003feac = uVar1;
  }
  else {
    *PTR_Pattern_EnabledIndex_0003feac = *PTR_DAT_0003feb4;
  }
  return;
}

