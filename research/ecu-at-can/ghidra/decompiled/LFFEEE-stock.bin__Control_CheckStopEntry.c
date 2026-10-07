/* Ghidra analysis output; verify against original SH instructions. */

/* Executed1280 coregatecases:722Aexact1->F972;elseif660E>660F OR6610>6611 return;elseF8D6.
   Unsignedbyteorder incl127/128checked. Terminalbody notstubbed; observationendsatentry. */

void Control_CheckStopEntry(void)

{
  undefined4 uVar1;
  char cVar2;
  
  uVar1 = (*(code *)PTR_FUN_0002c64c)(0x10);
  cVar2 = (*(code *)PTR_FUN_0002c694)(PTR_Control_FilteredModeInput_0002c690);
  if (cVar2 == '\x01') {
    (*(code *)PTR_FUN_0002c678)();
  }
  else if (((byte)*PTR_DAT_0002c650 <= (byte)*PTR_DAT_0002c65c) &&
          ((byte)*PTR_DAT_0002c658 <= (byte)*PTR_DAT_0002c660)) {
    (*(code *)PTR_FUN_0002c68c)();
  }
  (*(code *)PTR_FUN_0002c654)(uVar1);
  return;
}

