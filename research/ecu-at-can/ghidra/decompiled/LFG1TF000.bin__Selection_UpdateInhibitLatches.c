/* Ghidra analysis output; verify against original SH instructions. */

/* FullRAM/returnoracle: A735 nonzero/92C8bit5clear admits9C58bit0 set below signed80EA
   threshold7424or16640. 9415==1 clearsaux9C60bit2 andclearsmainonlyifA735==0;
   eitherlatchforcesreturn3. See tcu-inhibit-writers.txt. */

uint Selection_UpdateInhibitLatches(uint param_1)

{
  char cVar1;
  short sVar2;
  undefined *puVar3;
  char cVar4;
  byte bVar5;
  byte *pbVar6;
  
  puVar3 = PTR_Selection_InhibitFlags_00047d8c;
  bVar5 = *PTR_Selection_InhibitFlags_00047d8c & 1;
  cVar1 = *PTR_DAT_00047d90;
  cVar4 = (*(code *)PTR_FUN_00047d94)();
  if ((cVar1 != '\0') && ((*PTR_DAT_00047d98 & 0x20) == 0)) {
    if ((param_1 & 0xff) == 5) {
      param_1 = 4;
    }
    if (bVar5 == 0) {
      if ((*PTR_DAT_00047d9c & 8) == 0) {
        sVar2 = *(short *)PTR_Selection_InhibitUpperThreshold_00047da4;
      }
      else {
        sVar2 = *(short *)PTR_Selection_InhibitAlternateThreshold_00047da0;
      }
      if (DAT_ffff80ea < sVar2) {
        bVar5 = 1;
      }
    }
  }
  pbVar6 = (byte *)(int)DAT_00047d88;
  if (((((int)(char)*PTR_DAT_00047d9c & 0x80U) != 0) && ((*pbVar6 & 4) == 0)) &&
     (DAT_ffff80ea < *(short *)PTR_Selection_InhibitUpperThreshold_00047da4)) {
    *pbVar6 = *pbVar6 | 4;
  }
  if ((cVar4 == '\x01') && (*pbVar6 = *pbVar6 & 0xfb, cVar1 == '\0')) {
    bVar5 = 0;
  }
  if ((bVar5 == 1) || ((*(byte *)(int)DAT_00047d88 & 4) != 0)) {
    param_1 = 3;
  }
  if (bVar5 == 0) {
    bVar5 = *puVar3 & 0xfe;
  }
  else {
    bVar5 = *puVar3 | 1;
  }
  *puVar3 = bVar5;
  return param_1;
}

