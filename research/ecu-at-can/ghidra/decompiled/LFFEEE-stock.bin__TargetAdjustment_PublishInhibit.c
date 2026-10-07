/* Ghidra analysis output; verify against original SH instructions. */

/* Writes6954=(6561exact1 OR65AAexact1); otherrawbytesfalse.36directcases;
   control-target-adjustment.txt. */

char TargetAdjustment_PublishInhibit(void)

{
  char cVar1;
  
  cVar1 = '\x01';
  if ((*PTR_DAT_00030f38 == '\x01') || (cVar1 = *PTR_DAT_00030f3c, cVar1 == '\x01')) {
    *PTR_TargetAdjustment_Inhibit_00030f34 = 1;
  }
  else {
    *PTR_TargetAdjustment_Inhibit_00030f34 = 0;
  }
  return cVar1;
}

