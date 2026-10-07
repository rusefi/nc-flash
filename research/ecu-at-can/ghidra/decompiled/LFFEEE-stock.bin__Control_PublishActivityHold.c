/* Ghidra analysis output; verify against original SH instructions. */

/* Executed91E5=(unsigned91E4>0),1024cases and2 actualtask boundaries after77F12. Full mode0
   phases1/5 later stop at unsupported SCI0 initialization. */

void Control_PublishActivityHold(void)

{
  if (*PTR_Control_ActivityHoldCounter_00077f94 == '\0') {
    *DAT_00077fa0 = 0;
  }
  else {
    *DAT_00077fa0 = 1;
  }
  return;
}

