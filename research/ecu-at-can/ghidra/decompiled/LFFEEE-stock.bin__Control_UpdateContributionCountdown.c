/* Ghidra analysis output; verify against original SH instructions. */

/* 812Aexact1 andprevious8134zero reload8128=120;else decrementtozero. Publish8134=raw812A.80cases.
    */

void Control_UpdateContributionCountdown(void)

{
  char cVar1;
  undefined *puVar2;
  
  puVar2 = PTR_Control_PreviousFirstContributionGate_00059894;
  cVar1 = *PTR_Control_FirstContributionHysteresis_00059888;
  if ((*PTR_Control_PreviousFirstContributionGate_00059894 == '\0') && (cVar1 == '\x01')) {
    *PTR_Control_FirstContributionCountdown_00059898 = *PTR_DAT_0005989c;
  }
  else if (*PTR_Control_FirstContributionCountdown_00059898 != '\0') {
    *PTR_Control_FirstContributionCountdown_00059898 =
         *PTR_Control_FirstContributionCountdown_00059898 + (char)DAT_00059982;
  }
  *puVar2 = cVar1;
  return;
}

