/* Ghidra analysis output; verify against original SH instructions. */

/* Returns u16(92EE)>>7, usedagainststockbyte9 forcurvebank. No physicalunits. */

ushort ClassBase_ReadShiftedWord(void)

{
  return *DAT_0003af28 >> 7;
}

