/* Ghidra analysis output; verify against original SH instructions. */

/* Executedall256bytes via1617E/2C3CC:6611 incrementsmod256; schedulingcadenceunproved. */

void Control_IncrementSecondActivityEnd(void)

{
  undefined *puVar1;
  undefined4 uVar2;
  
  uVar2 = (*(code *)PTR_FUN_0002c64c)(0x10);
  puVar1 = PTR_FUN_0002c654;
  *PTR_DAT_0002c660 = *PTR_DAT_0002c660 + '\x01';
  (*(code *)puVar1)(uVar2);
  return;
}

