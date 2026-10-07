/* Ghidra analysis output; verify against original SH instructions. */

/* 9462 exact1 OR8F38 exact1 clears8F33..36/8F30, retains8F37. Else zero8F2C..2F sets corresponding
   latch1; nonzero retains. Only8F35/36 exact1 sets8F30=1 and8F37=0; else retains both.2048 cases
   and320 retained cycles. Input identities/writers open. Upstream6D876 now verified to clear
   fallback on inclusive8..248 recovery; see control-raw-provenance.txt. */

char Control_UpdateRawFallbackLatches(void)

{
  undefined *puVar1;
  undefined *puVar2;
  char cVar3;
  
  puVar1 = PTR_DAT_0006da84;
  cVar3 = (*(code *)PTR_FUN_0006da8c)(PTR_DAT_0006da88);
  if ((cVar3 == '\x01') || (*PTR_DAT_0006da90 == '\x01')) {
    cVar3 = '\x01';
    *puVar1 = 0;
    *PTR_DAT_0006da94 = 0;
    *PTR_DAT_0006da98 = 0;
    *PTR_DAT_0006da9c = 0;
    *PTR_Control_RawSecondFallbackLatch_0006daa0 = 0;
  }
  else {
    if (*PTR_DAT_0006daa4 == '\0') {
      *PTR_DAT_0006da98 = 1;
    }
    if (*PTR_DAT_0006daa8 == '\0') {
      *PTR_DAT_0006da9c = 1;
    }
    if (*PTR_DAT_0006daac == '\0') {
      *puVar1 = 1;
    }
    if (*PTR_DAT_0006dab0 == '\0') {
      *PTR_DAT_0006da94 = 1;
    }
    puVar2 = PTR_DAT_0006dab4;
    cVar3 = '\x01';
    if ((*puVar1 == '\x01') || (cVar3 = *PTR_DAT_0006da94, cVar3 == '\x01')) {
      *PTR_Control_RawSecondFallbackLatch_0006daa0 = 1;
      *puVar2 = 0;
    }
  }
  return cVar3;
}

