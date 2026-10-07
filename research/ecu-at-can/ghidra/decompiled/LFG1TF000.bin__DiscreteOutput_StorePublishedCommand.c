/* Ghidra analysis output; verify against original SH instructions. */

/* WriteslowbyteR5 to8A1C+u8R4; original52D8C completebodyexecuted. See tcu-source-inhibit.txt. */

void DiscreteOutput_StorePublishedCommand(uint param_1,undefined1 param_2)

{
  *(undefined1 *)((param_1 & 0xff) + (int)DAT_00018742) = param_2;
  return;
}

