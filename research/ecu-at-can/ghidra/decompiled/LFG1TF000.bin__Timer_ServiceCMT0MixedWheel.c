/* Ghidra analysis output; verify against original SH instructions. */

/* Mixedincrement/decrement rangebanks and3-tierphasewheel, NOTonlycountdown. Independent8000
   wholeRAM cases coverall1000 validphase triples/eightboundarypatterns;
   bankcounts8000/1600/800/80/8. Stock5C170/198/1C0 and76D24..76DC3 asserted.
   JoinedCMT0prefix320/32000events plus320 independenttimerstate replays PASS;
   tcu-cmt0-delivery.txt. Hardwarecadence unproved. */

void Timer_ServiceCMT0MixedWheel(void)

{
  byte *pbVar1;
  
  Timer_ServiceFirstRanges();
  pbVar1 = (byte *)(int)DAT_00011b4a;
  (**(code **)(PTR_PTR_00011b50 + (uint)*pbVar1 * 4))();
  *pbVar1 = *pbVar1 + 1;
  if (*pbVar1 == 10) {
    *pbVar1 = 0;
  }
  return;
}

