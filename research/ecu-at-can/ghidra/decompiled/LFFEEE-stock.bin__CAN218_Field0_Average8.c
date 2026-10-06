/* Ghidra analysis output; verify against original SH instructions. */

/* Averages eight received normalized field0 samples; physical role unresolved. */

void CAN218_Field0_Average8(void)

{
  undefined4 *puVar1;
  float *pfVar2;
  char cVar3;
  byte bVar4;
  undefined4 *puVar5;
  undefined4 uVar6;
  float fVar7;
  float fVar8;
  
  pfVar2 = (float *)PTR_DAT_0002f094;
  cVar3 = '\a';
  puVar1 = (undefined4 *)(PTR_DAT_0002f094 + 0x18);
  uVar6 = *(undefined4 *)PTR_CAN218_Field0_0002f090;
  puVar5 = (undefined4 *)(PTR_DAT_0002f094 + 0x20);
  do {
    cVar3 = cVar3 + -1;
    puVar5 = puVar5 + -1;
    *puVar5 = *puVar1;
    puVar1 = puVar1 + -1;
  } while (cVar3 != '\0');
  if (*PTR_DAT_0002f098 == '\x01') {
    *pfVar2 = 0.0;
  }
  else {
    *pfVar2 = (float)uVar6;
  }
  bVar4 = 0;
  fVar7 = 0.0;
  do {
    bVar4 = bVar4 + 1;
    fVar8 = *pfVar2;
    pfVar2 = pfVar2 + 1;
    fVar7 = fVar8 + fVar7;
  } while (bVar4 < 8);
  *(float *)PTR_DAT_0002f0a0 = fVar7 * DAT_0002f09c;
  return;
}

