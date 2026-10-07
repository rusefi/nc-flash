/* Ghidra analysis output; verify against original SH instructions. */

/* WriteslowbyteR5 toA5C5+u8R4; original1F3CE suppliesfive0/1commands. See tcu-source-inhibit.txt.
    */

void DiscreteOutput_SetCommand(uint param_1,undefined1 param_2)

{
  *(undefined1 *)((param_1 & 0xff) + (int)DAT_00052e40) = param_2;
  return;
}

