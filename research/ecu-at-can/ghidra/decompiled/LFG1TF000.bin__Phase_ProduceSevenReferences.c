/* Ghidra analysis output; verify against original SH instructions. */

/* Seven signed32 references9218[i] = floor(s16(80EC)*s16(70000[i])/4096), original signed-word
   multiply/12 arithmetic shifts;526 inputs/3682 word checks, MACL preserved. Full2086C source now
   executed from capture0A through paired shifts in tcu-reference-source.txt; physical identity
   open. Full126EC capture experiment observes actualphase0/4 call after2086C; code0 target14455
   at80EC7017. See tcu-captured-requests.txt. */

void Phase_ProduceSevenReferences(void)

{
  undefined4 uVar1;
  undefined4 *puVar2;
  undefined4 *puVar3;
  
  puVar3 = (undefined4 *)(PTR_Phase_ProducedReferenceWords_000211b4 + 0x1c);
  puVar2 = (undefined4 *)PTR_Phase_ProducedReferenceWords_000211b4;
  do {
    uVar1 = (*(code *)PTR_FixedPoint_ShiftSignedBy12_000211b8)();
    *puVar2 = uVar1;
    puVar2 = puVar2 + 1;
  } while (puVar2 < puVar3);
                    /* WARNING: Could not recover jumptable at 0x000211aa. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*(code *)PTR_LAB_000211bc)();
  return;
}

