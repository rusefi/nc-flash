/* Ghidra analysis output; verify against original SH instructions. */

/* Stores lowbyteR4 to8A18 withoutnormalization. Direct1->2->0 failsPWMreselect; normal529AC
   emitsbinaryonly. See tcu-output-pin-switch.txt. */

void OutputPins_StoreCommand(undefined1 param_1)

{
  *(undefined1 *)(int)DAT_00018642 = param_1;
  return;
}

