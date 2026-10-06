/* Ghidra analysis output; verify against original SH instructions. */

/* Initializes 843E and 8440 to FFFF sentinel; used in executed missing-input countdown and recovery
   fixtures. */

void Selector_InitializeDiagnosticTimers(void)

{
  undefined *puVar1;
  undefined2 uVar2;
  
  puVar1 = PTR_DAT_00058600;
  uVar2 = SUB42(PTR_DAT_000585f8,0);
  *(undefined2 *)PTR_DAT_000585fc = uVar2;
  *(undefined2 *)puVar1 = uVar2;
  return;
}

