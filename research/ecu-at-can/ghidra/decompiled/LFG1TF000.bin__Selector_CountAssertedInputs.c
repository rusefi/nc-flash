/* Ghidra analysis output; verify against original SH instructions. */

/* Adds signed bytes 88B4..88B7; physical connector mapping unproven. */

int Selector_CountAssertedInputs(void)

{
  return (int)(char)*PTR_Selector_FilteredInputZero_000586d4 + (int)(char)*PTR_DAT_000586d8 +
         (int)(char)*PTR_Selector_FilteredInputTwo_000586dc + (int)(char)*PTR_DAT_000586e0;
}

