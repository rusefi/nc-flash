/* Ghidra analysis output; verify against original SH instructions. */

/* Stores R5 byte atA9DC+unsigned R4. Receive groups36/37/38 map to21/22/23 through5EB84 table.
   Consumers/fallback unresolved. */

void Diagnostic_StoreMappedStatus(uint param_1,undefined1 param_2)

{
  *(undefined1 *)((param_1 & 0xff) + (int)DAT_00058006) = param_2;
  return;
}

