/* Ghidra analysis output; verify against original SH instructions. */

/* Executed1024 cases:returns1 iffA55C!=1 and2B84==1. Plainbytepredicate,noRAMwrites; usedby74D62.
    */

undefined4 Control_CheckActivityReadEligibility(void)

{
  undefined4 uVar1;
  
  if (*PTR_DAT_000144a4 == '\x01') {
    uVar1 = 0;
  }
  else if (*PTR_DAT_000144a8 == '\x01') {
    uVar1 = 1;
  }
  else {
    uVar1 = 0;
  }
  return uVar1;
}

