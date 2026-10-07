/* Ghidra analysis output; verify against original SH instructions. */

/* Executed: abs(6D5C)>1.8839999437332153 or9462 reset reload8EDC=30; otherwise positive decrement.
   Physical units and timing unproved. */

uint LocalInputDiag_UpdateActivityHold(void)

{
  undefined *puVar1;
  undefined *puVar2;
  char cVar5;
  uint uVar3;
  uint uVar4;
  float fVar6;
  
  fVar6 = (float)(*(code *)PTR_FUN_0006c9f4)(PTR_SpeedCandidate_ProtectedSelected_0006c9f0);
  cVar5 = (*(code *)PTR_FUN_0006ca00)(fVar6,0,DAT_0006c9fc);
  uVar3 = (*(code *)PTR_FUN_0006ca08)(PTR_DAT_0006ca04);
  puVar1 = PTR_DAT_0006ca0c;
  uVar4 = uVar3;
  if ((cVar5 == '\0') && (uVar4 = 1, (uVar3 & 0xff) != 1)) {
    uVar4 = (uint)(byte)*PTR_DAT_0006ca0c;
    if (uVar4 != 0) {
      *PTR_DAT_0006ca0c = *PTR_DAT_0006ca0c + (char)DAT_0006c9e6;
    }
  }
  else {
    *PTR_DAT_0006ca0c = *PTR_DAT_0006ca10;
  }
  puVar2 = PTR_DAT_0006ca14;
  if (*PTR_DAT_0006ca14 == '\0') {
    *PTR_DAT_0006ca18 = 0;
  }
  else if (*(float *)PTR_DAT_0006ca20 < *(float *)PTR_DAT_0006ca1c) {
    uVar4 = 1;
    *PTR_DAT_0006ca18 = 1;
  }
  if ((*puVar1 == '\0') || (uVar4 = uVar3 & 0xff, uVar4 == 1)) {
    *puVar2 = 0;
  }
  else if (*(float *)PTR_DAT_0006ca24 < fVar6) {
    *puVar2 = 1;
  }
  return uVar4;
}

