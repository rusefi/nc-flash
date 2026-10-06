/* Ghidra analysis output; verify against original SH instructions. */

/* Scans group active04 and record flags01/40 plus stored80;532C8 writes aggregateA666. Clears after
   tested healthy recovery whileA99B persists; 5329A/532D8 selects startup/override ->A665 ->CAN231
   byte1 bit6. */

void Diagnostic_UpdateActiveAggregate(void)

{
  bool bVar1;
  byte bVar2;
  char acStack_1c [8];
  
  bVar1 = false;
  for (bVar2 = 1; (!bVar1 && (bVar2 < 0x49)); bVar2 = bVar2 + 1) {
    (*(code *)PTR_FUN_00057238)(acStack_1c,(uint)bVar2 * 2 + DAT_00057234 + 0x4b,2);
    if ((PTR_DAT_0005723c[bVar2] & 4) != 0) {
      if (((PTR_Diagnostic_GroupConfiguration_00057240[(uint)bVar2 * 0x10 + 7] & 1) != 0) &&
         (((PTR_Diagnostic_GroupConfiguration_00057240[(uint)bVar2 * 0x10 + 7] & 0x40) != 0 ||
          (((int)acStack_1c[0] & 0x80U) != 0)))) {
        bVar1 = true;
      }
    }
  }
  (*(code *)PTR_FUN_00057244)(bVar1);
  return;
}

