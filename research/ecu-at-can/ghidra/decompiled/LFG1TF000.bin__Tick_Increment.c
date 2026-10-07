/* Ghidra analysis output; verify against original SH instructions. */

/* IncrementsFFFF84D0 via CMT0 chain. Directoriginalcalls advance192fulltaskreceive-deadline
   experiment;11014 alone doesNOTadvance84D0. Explicitinterleave, notphysicalclockperiod. See
   tcu-receive-admission.txt. NativeCMT0 alsoadvances91AC and11A64 countdownwheel; directtickalone
   omits thoseeffects. tcu-cmt0-interrupt.txt. */

void Tick_Increment(void)

{
  *(int *)(int)DAT_00011954 = *(int *)(int)DAT_00011954 + 1;
  return;
}

