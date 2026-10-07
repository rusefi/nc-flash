/* Ghidra analysis output; verify against original SH instructions. */

/* Originalbodyreturns55555555 in8wholeRAM fixtures andinitializerprefixPR28CA4. Testsinteger/FPU
   operations includingdeliberate0/0,unorderedcomparisons,stickyFPSCR40. Writes6418/641C=41CCCCCA.
   BoundedlocalFPUmodel;notphysicalCPU/fullboot proof. control-initialize-fpu.txt. */

void CPU_RunInstructionSelfTest(void)

{
                    /* WARNING: Could not recover jumptable at 0x00028e12. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*(code *)PTR_LAB_00029008)();
  return;
}

