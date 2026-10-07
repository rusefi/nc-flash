/* Ghidra analysis output; verify against original SH instructions. */

/* Originalcaller runs22F46 then tails230F0.1800 randomized paired cases check both independent
   models and balanced stack; tcu-paired-input.txt. */

void Input_UpdatePairedHistories(void)

{
  Primary_UpdateInputAndHistory();
  Comparison_UpdateInputAndHistory();
  return;
}

