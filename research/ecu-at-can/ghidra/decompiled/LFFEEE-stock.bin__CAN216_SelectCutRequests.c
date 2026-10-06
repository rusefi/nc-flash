/* Ghidra analysis output; verify against original SH instructions. */

/* Bit5 ->6E62; word2 window ->6E63. Stock B81B3=0 selects231 bit4 for6E64. */

undefined4 CAN216_SelectCutRequests(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined4 uVar3;
  char cVar4;
  
  *PTR_DAT_0003b688 = 0;
  puVar1 = PTR_FUN_0003b68c;
  (*(code *)PTR_FUN_0003b68c)(PTR_DAT_0003b690,0);
  puVar2 = PTR_DAT_0003b698;
  if ((*PTR_TransmissionModeFlags_0003b65c & 0x40) == 0) {
    if (*PTR_CAN216_Bit5CutRequest_0003b6a0 == '\x01') {
      *PTR_ATCutRequestBothPairs_0003b694 = 1;
    }
    else {
      *PTR_ATCutRequestBothPairs_0003b694 = 0;
    }
    if (*PTR_DAT_0003b6a4 == '\x01') {
      *puVar2 = 1;
    }
    else {
      *puVar2 = 0;
    }
    if (*PTR_DAT_0003b6a8 == '\0') {
      if ((*PTR_DAT_0003b6b0 == '\x01') &&
         (cVar4 = (*(code *)PTR_FUN_0003b6b8)(PTR_DAT_0003b6b4), cVar4 == '\x01')) {
        uVar3 = 1;
      }
      else {
        uVar3 = 0;
      }
      uVar3 = (*(code *)puVar1)(PTR_DAT_0003b69c,uVar3);
    }
    else {
      uVar3 = (*(code *)puVar1)(PTR_DAT_0003b69c,*PTR_DAT_0003b6ac != '\0');
    }
  }
  else {
    *PTR_ATCutRequestBothPairs_0003b694 = 0;
    *puVar2 = 0;
    uVar3 = (*(code *)puVar1)(PTR_DAT_0003b69c,0);
  }
  return uVar3;
}

