/* Ghidra analysis output; verify against original SH instructions. */

/* Normal3054E priority/allocation scan ->98D4/98D6,98B2. Qualified92C8bit6 overrides0 or15232
   preservingselection. Publishes9108 via1F292 or7FFF via1F29E;98ACbits0/4; tail39B56
   executes.288cases/400tailchecks. */

void ClassApplication_SelectAndPublish(void)

{
  bool bVar1;
  bool bVar2;
  undefined *puVar3;
  byte bVar4;
  short *psVar5;
  
  puVar3 = PTR_DAT_00039d5c;
  bVar1 = false;
  if (((DAT_ffff800e < 0x3c) || ('\x03' < (char)*PTR_Primary_CompressedCategory_00039d58)) ||
     (CAN231_SixStateSource != 5)) {
    bVar1 = true;
  }
  psVar5 = (short *)(int)DAT_00039d44;
  bVar2 = false;
  if (((*PTR_DAT_00039d5c & 0x40) == 0) || (bVar1)) {
    (*(code *)PTR_RequestList_SelectCandidate_00039d70)
              (PTR_ClassApplication_PriorityList_00039d48,PTR_DAT_00039d4c,PTR_DAT_00039d6c,
               PTR_DAT_00039d68);
    *psVar5 = *(short *)PTR_DAT_00039d6c;
  }
  else {
    *psVar5 = *(short *)PTR_PTR_00039d60;
    bVar2 = true;
    if ((*puVar3 & 0x10) != 0) {
      *psVar5 = *(short *)PTR_DAT_00039d64;
    }
  }
  if (*psVar5 == -1) {
    (*(code *)PTR_FUN_00039d54)(0);
  }
  else {
    (*(code *)PTR_FUN_00039d74)(0);
  }
  puVar3 = PTR_DAT_00039d78;
  if (bVar1) {
    bVar4 = *PTR_DAT_00039d78 | 1;
  }
  else {
    bVar4 = *PTR_DAT_00039d78 & 0xfe;
  }
  *PTR_DAT_00039d78 = bVar4;
  if (bVar2) {
    bVar4 = *puVar3 | 0x10;
  }
  else {
    bVar4 = *puVar3 & 0xef;
  }
  *puVar3 = bVar4;
  ClassApplication_RetainBandState();
  return;
}

