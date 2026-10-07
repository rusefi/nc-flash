/* Ghidra analysis output; verify against original SH instructions. */

/* Clears8A18/8A19;141BC stockdescriptor5C500 withflag0 setsPFDRbit14. DoesnotreselectPWM. See
   tcu-output-pin-switch.txt. */

void OutputPins_InitCommand(void)

{
  undefined *puVar1;
  undefined1 *puVar2;
  
  puVar1 = PTR_DAT_00018648;
  puVar2 = (undefined1 *)(int)DAT_00018644;
  *(undefined1 *)(int)DAT_00018642 = 0;
  *puVar2 = 0;
  (*(code *)PTR_PortOutput_WriteDescriptor_0001864c)(puVar1,0);
  return;
}

