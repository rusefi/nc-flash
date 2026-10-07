/* Ghidra analysis output; verify against original SH instructions. */

/* u16 932C/932E ->floor(10*x/256) to80A4/80BA, A4FA->A4FC.65536directvalues
   plus40actualwholeRAMreturns in160 stoppedcapturetasks. 80A4 remains329 aftermeasurementzero
   due80EA3070; activefaultretained. tcu-receive-recovery.txt. */

void Diagnostic_ScaleTwoApplicationWords(void)

{
  DAT_ffff80a4 = (undefined2)((uint)*DAT_00050f5c * 5 >> 7);
  DAT_ffff80ba = (undefined2)((uint)*(ushort *)PTR_DAT_00050f60 * 5 >> 7);
  *PTR_DAT_00050f58 = *PTR_DAT_00050f64;
  return;
}

