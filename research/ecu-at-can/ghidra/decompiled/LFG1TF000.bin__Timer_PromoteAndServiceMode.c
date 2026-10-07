/* Ghidra analysis output; verify against original SH instructions. */

/* Promotes8009 from1 to3 then calls12886; every byte mode executed. NativeCMT1prefix nowverifies
   status/mode admission andwholeRAM primarywheel effects; tcu-cmt1-delivery.txt. */

void Timer_PromoteAndServiceMode(void)

{
  if (DAT_ffff8009 == '\x01') {
    DAT_ffff8009 = '\x03';
  }
  (*(code *)PTR_Timer_ServiceWhenMode3_000123ac)();
  return;
}

