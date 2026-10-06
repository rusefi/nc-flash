/* Ghidra analysis output; verify against original SH instructions. */

/* WARNING: Removing unreachable block (ram,0x00045f56) */
/* Sample74F1 bit7492 ->749A;nonzero cylinder clears749E+c mask40 and records activity749B.7534
   history/countdown separate.8192 pattern and243 gate/history cases. */

byte Pattern_SampleAndClearCylinder(void)

{
  byte bVar1;
  char cVar2;
  byte bVar3;
  char cVar4;
  undefined *puVar5;
  
  bVar1 = *PTR_Pattern_EventCylinder_00045ef8;
  bVar3 = *PTR_DAT_00045ef0;
  cVar2 = *PTR_DAT_00045f1c;
  if (bVar3 == 1) {
    puVar5 = PTR_Pattern_CurrentEventInhibit_00045f20;
    bVar3 = (*(code *)PTR_FUN_00045f24)();
    if ((*PTR_Pattern_EventMask_00045f28 & bVar3) == 0) {
      *puVar5 = 0;
    }
    else {
      *puVar5 = 1;
    }
    if (bVar1 != 0) {
      cVar4 = (*(code *)PTR_FUN_00045f10)(PTR_DAT_00045f0c);
      if (cVar4 == '\x01') {
        *PTR_Pattern_PreviousActive_00045f14 = 1;
      }
      else {
        *PTR_Pattern_PreviousActive_00045f14 = 0;
      }
    }
    puVar5 = PTR_Pattern_Previous7534_00045f2c;
    bVar3 = *PTR_Pattern_Previous7534_00045f2c;
    if ((bVar3 == 1) && (cVar2 == '\0')) {
      *PTR_Pattern_EventHistoryCountdown_00045f30 = 10;
    }
    else if (*PTR_Pattern_EventHistoryCountdown_00045f30 != '\0') {
      *PTR_Pattern_EventHistoryCountdown_00045f30 =
           *PTR_Pattern_EventHistoryCountdown_00045f30 + (char)DAT_00046018;
    }
    if (bVar1 != 0) {
      bVar3 = PTR_DAT_0004601c[bVar1] & 0xbf;
      PTR_DAT_0004601c[bVar1] = bVar3;
    }
    *puVar5 = cVar2;
  }
  return bVar3;
}

