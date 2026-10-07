/* Ghidra analysis output; verify against original SH instructions. */

/* A5A0=8A18=1 ifeitherA5A1/A5A2 exactly1,else0. ImmediateA5A0 fallbackproducer verified;
   fullscheduler open. See tcu-output-pin-switch.txt. */

void OutputPins_ArbitrateSources(void)

{
  char *pcVar1;
  char cVar2;
  
  cVar2 = '\0';
  if ((*(char *)(int)DAT_000529f2 == '\x01') || (*(char *)(int)DAT_000529f4 == '\x01')) {
    cVar2 = '\x01';
  }
  pcVar1 = (char *)(int)DAT_000529f0;
  *pcVar1 = cVar2;
  (*(code *)PTR_OutputPins_StoreCommand_000529f8)((int)*pcVar1);
  return;
}

