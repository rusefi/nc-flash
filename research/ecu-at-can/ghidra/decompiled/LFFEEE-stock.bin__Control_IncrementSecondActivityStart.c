/* Ghidra analysis output; verify against original SH instructions. */

/* Executedall256bytes via16172/2C39C:6610 incrementsmod256; usedby2C4FC/2C5DE. */

void Control_IncrementSecondActivityStart(void)

{
  undefined *puVar1;
  undefined4 uVar2;
  
  uVar2 = (*(code *)PTR_FUN_0002c64c)(0x10);
  puVar1 = PTR_FUN_0002c654;
  *PTR_DAT_0002c658 = *PTR_DAT_0002c658 + '\x01';
  (*(code *)puVar1)(uVar2);
  return;
}

