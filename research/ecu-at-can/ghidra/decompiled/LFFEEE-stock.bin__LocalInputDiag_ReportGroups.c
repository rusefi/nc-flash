/* Ghidra analysis output; verify against original SH instructions. */

/* Executed groups43/P0704 and44/P0850; pass mode2 priority. Real cache writes, but stock AC008
   masks0000 reject downstream dispatch. See local-input-faults.txt. */

uint LocalInputDiag_ReportGroups(void)

{
  undefined *puVar1;
  uint uVar2;
  
  puVar1 = PTR_Diagnostic_ReportUntimedGroup_0006c258;
  if (*PTR_DAT_0006c25c == '\x01') {
    (*(code *)PTR_Diagnostic_ReportUntimedGroup_0006c258)(0x43,2);
  }
  else if (*PTR_LocalInputDiag_ClutchFault_0006c260 == '\x01') {
    (*(code *)PTR_Diagnostic_ReportUntimedGroup_0006c258)(0x43,1);
  }
  if (*PTR_DAT_0006c264 == '\x01') {
    uVar2 = (*(code *)puVar1)(0x44,2);
  }
  else {
    uVar2 = (uint)(byte)*PTR_LocalInputDiag_NeutralFault_0006c268;
    if (uVar2 == 1) {
      uVar2 = (*(code *)puVar1)(0x44,1);
    }
  }
  return uVar2;
}

