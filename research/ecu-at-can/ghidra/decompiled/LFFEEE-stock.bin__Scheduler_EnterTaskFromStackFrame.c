/* Ghidra analysis output; verify against original SH instructions. */

/* Executed prefix constructs new task frame bySP=R5,pushSR0,pushentryR4,RTE3F3C/NOP.
   LocalboundedRTE checked456cases/7rejections againstSH2E manual7.2.48. No interrupt generation or
   physical timing simulation. */

void Scheduler_EnterTaskFromStackFrame(undefined4 param_1,int param_2)

{
  *(undefined4 *)(param_2 + -4) = 0;
  *(undefined4 *)(param_2 + -8) = param_1;
  return;
}

