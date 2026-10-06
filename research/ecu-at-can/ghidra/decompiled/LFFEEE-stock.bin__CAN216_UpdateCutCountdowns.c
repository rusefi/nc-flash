/* Ghidra analysis output; verify against original SH instructions. */

/* Six local gates; rising requests load100 from B81AE/AF, subsequent calls decrement without
   reloading held request. */

uint CAN216_UpdateCutCountdowns(void)

{
  char cVar1;
  char cVar2;
  undefined *puVar3;
  undefined *puVar4;
  char cVar6;
  uint uVar5;
  
  puVar4 = PTR_DAT_0003add4;
  puVar3 = PTR_DAT_0003add0;
  cVar1 = *PTR_DAT_0003add0;
  cVar2 = *PTR_DAT_0003add4;
  if (((((*PTR_DAT_0003add8 == '\x01') && (*PTR_DAT_0003addc == '\0')) &&
       (*PTR_DAT_0003ade0 == '\x01')) &&
      ((cVar6 = (*(code *)PTR_FUN_0003ade8)(PTR_DAT_0003ade4), cVar6 == '\x01' &&
       (*PTR_DAT_0003adec == '\0')))) && (*PTR_DAT_0003adf0 == '\x01')) {
    if ((*PTR_ATCutRequestBothPairs_0003adf4 == '\x01') && (*PTR_DAT_0003adf8 != '\0')) {
      *puVar3 = 1;
    }
    else {
      *puVar3 = 0;
    }
    if (((*PTR_DAT_0003adfc == '\x01') || (*PTR_ATCutRequestBothPairs_0003adf4 == '\x01')) &&
       (*PTR_DAT_0003ae00 != '\0')) {
      *puVar4 = 1;
    }
    else {
      *puVar4 = 0;
    }
  }
  else {
    *puVar3 = 0;
    *puVar4 = 0;
  }
  uVar5 = (uint)cVar1;
  cVar1 = (char)DAT_0003adcc;
  if ((uVar5 == 0) && (uVar5 = (uint)(byte)*PTR_DAT_0003add0, uVar5 == 1)) {
    *PTR_ATCutCountdownPair23_0003ae04 = *PTR_DAT_0003ae08;
  }
  else if (*PTR_ATCutCountdownPair23_0003ae04 != '\0') {
    *PTR_ATCutCountdownPair23_0003ae04 = *PTR_ATCutCountdownPair23_0003ae04 + cVar1;
  }
  if ((cVar2 == '\0') && (uVar5 = (uint)(byte)*PTR_DAT_0003b00c, uVar5 == 1)) {
    *PTR_ATCutCountdownPair14_0003b008 = *PTR_DAT_0003b010;
  }
  else if (*PTR_ATCutCountdownPair14_0003b008 != '\0') {
    *PTR_ATCutCountdownPair14_0003b008 = *PTR_ATCutCountdownPair14_0003b008 + cVar1;
  }
  return uVar5;
}

