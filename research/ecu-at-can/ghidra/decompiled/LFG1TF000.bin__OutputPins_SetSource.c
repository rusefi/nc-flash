/* Ghidra analysis output; verify against original SH instructions. */

/* Selectorlowbyte0 writeslowbyteR5 toA5A1;1 writesA5A2;otherspreserve. 1280selector/valuecases. See
   tcu-output-pin-switch.txt. */

char OutputPins_SetSource(char param_1,undefined1 param_2)

{
  if (param_1 == '\0') {
    *(undefined1 *)(int)DAT_000529f2 = param_2;
    return '\0';
  }
  if (param_1 != '\x01') {
    return param_1;
  }
  *(undefined1 *)(int)DAT_000529f4 = param_2;
  return '\x01';
}

