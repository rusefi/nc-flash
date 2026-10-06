/* Ghidra analysis output; verify against original SH instructions. */

/* Valid groups1..48(hex) call5752E,5743C,57A32. Creates memory reporting state/list; EEPROM
   durability unverified. */

void Diagnostic_RecordQualifiedGroup(uint param_1)

{
  if (((param_1 & 0xff) != 0) && ((param_1 & 0xff) < 0x49)) {
    FUN_0005752e(param_1);
    FUN_0005743c(param_1);
    (*(code *)PTR_FUN_0005746c)(param_1);
    return;
  }
  return;
}

