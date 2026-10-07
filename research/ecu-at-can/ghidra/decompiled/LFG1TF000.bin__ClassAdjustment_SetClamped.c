/* Ghidra analysis output; verify against original SH instructions. */

/* Signed32R4value,classR5;clampstock+/-80 then2456Eknownclass0..2.
   Markersunchanged.36B26uniformshift executesgetter/setterloop. */

void ClassAdjustment_SetClamped(int param_1,int param_2)

{
  if (*(short *)PTR_DAT_00036e68 < param_1) {
    param_1 = (int)*(short *)PTR_DAT_00036e68;
  }
  if (param_1 < *(short *)PTR_DAT_00036e6c) {
    param_1 = (int)*(short *)PTR_DAT_00036e6c;
  }
                    /* WARNING: Could not recover jumptable at 0x00036e40. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*(code *)PTR_StoredWord_WriteAdjustment_00036e70)
            ((int)*(short *)(PTR_DAT_00036e60 + param_2 * 2),param_1);
  return;
}

