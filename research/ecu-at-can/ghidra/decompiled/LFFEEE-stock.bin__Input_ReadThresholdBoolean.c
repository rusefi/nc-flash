/* Ghidra analysis output; verify against original SH instructions. */

/* Executed unsigned word401C >=8000 -> Boolean; physical source unproved. */

bool Input_ReadThresholdBoolean(void)

{
  return (int)PTR_LAB_0000cbe0 <= (int)(uint)*DAT_0000cbdc;
}

