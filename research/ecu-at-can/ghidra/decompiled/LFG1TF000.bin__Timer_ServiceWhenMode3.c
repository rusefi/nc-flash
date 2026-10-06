/* Ghidra analysis output; verify against original SH instructions. */

/* Only8009==3 tail-calls11014; every byte mode executed. */

uint Timer_ServiceWhenMode3(void)

{
  uint uVar1;
  
  uVar1 = (uint)DAT_ffff8009;
  if ((uVar1 != 1) && (uVar1 == 3)) {
    uVar1 = (*(code *)PTR_Timer_ServicePrimaryWheel_000128a4)();
    return uVar1;
  }
  return uVar1;
}

