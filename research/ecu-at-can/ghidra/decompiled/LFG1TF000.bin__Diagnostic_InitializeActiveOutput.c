/* Ghidra analysis output; verify against original SH instructions. */

/* Initializes A666=0,A664=A665=1,8464=0,A667=A668=0. Startup indication is independent of stored
   MIL status. */

void Diagnostic_InitializeActiveOutput(void)

{
  undefined *puVar1;
  undefined *puVar2;
  
  puVar2 = PTR_DAT_000532f8;
  puVar1 = PTR_DAT_000532f4;
  *(undefined1 *)(int)DAT_000532ee = 0;
  *(undefined2 *)puVar1 = 0;
  *puVar2 = 1;
  *PTR_DAT_000532fc = 1;
  *(undefined1 *)(int)DAT_000532f0 = 0;
  *(undefined1 *)(int)DAT_000532f2 = 0;
  return;
}

