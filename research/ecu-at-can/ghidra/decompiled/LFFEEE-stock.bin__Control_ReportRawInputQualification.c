/* Ghidra analysis output; verify against original SH instructions. */

/* Executed9984wholeRAM cases:8EFF exact1 emits groups1F/20 mode2;else8EFB/8EFC exact1 emits
   corresponding mode1. Original report/cache callees execute. Cache-only admission scope; physical
   roles and stored-DTC lifecycle unproved. */

uint Control_ReportRawInputQualification(void)

{
  undefined *puVar1;
  uint uVar2;
  
  puVar1 = PTR_Diagnostic_ReportUntimedGroup_0006d024;
  if (*PTR_DAT_0006d028 == '\x01') {
    (*(code *)PTR_Diagnostic_ReportUntimedGroup_0006d024)(0x1f,2);
    uVar2 = (*(code *)puVar1)(0x20,2);
  }
  else {
    if (*PTR_DAT_0006d02c == '\x01') {
      (*(code *)PTR_Diagnostic_ReportUntimedGroup_0006d024)(0x1f,1);
    }
    uVar2 = (uint)(byte)*PTR_DAT_0006d030;
    if (uVar2 == 1) {
      uVar2 = (*(code *)puVar1)(0x20,1);
    }
  }
  return uVar2;
}

