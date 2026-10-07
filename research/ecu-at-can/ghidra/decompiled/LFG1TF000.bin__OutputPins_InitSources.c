/* Ghidra analysis output; verify against original SH instructions. */

/* ClearsA5A0/A5A1/A5A2 andtail1863C setscommand0. Doesnotdirectlyselectpins. See
   tcu-output-pin-switch.txt. */

void OutputPins_InitSources(void)

{
  undefined *puVar1;
  undefined1 *puVar2;
  
  puVar2 = (undefined1 *)(int)DAT_000529f2;
  *(undefined1 *)(int)DAT_000529f0 = 0;
  *puVar2 = 0;
  puVar1 = PTR_OutputPins_StoreCommand_000529f8;
  *(undefined1 *)(int)DAT_000529f4 = 0;
  (*(code *)puVar1)(0);
  return;
}

