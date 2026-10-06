/* Ghidra analysis output; verify against original SH instructions. */

/* Action4 setsA6EC+group bit04 clears02, calls57374 and aggregate5701A. Action0 clears06/80. Tested
   in fourteen paired lifecycles. */

void Diagnostic_UpdateActiveGroup(uint param_1,char param_2)

{
  undefined *puVar1;
  byte *pbVar2;
  
  pbVar2 = (byte *)((param_1 & 0xff) + DAT_00056a08);
  if (param_2 == '\x02') {
    *pbVar2 = *pbVar2 | 2;
  }
  else if (param_2 == '\x04') {
    *pbVar2 = *pbVar2 | 4;
    puVar1 = PTR_Diagnostic_RecordQualifiedGroup_00056ac0;
    *pbVar2 = *pbVar2 & 0xfd;
    (*(code *)puVar1)(param_1);
    FUN_00056a86(param_1);
  }
  else if (param_2 == '\0') {
    *pbVar2 = *pbVar2 & 0xf9;
    *pbVar2 = *pbVar2 & 0x7f;
  }
                    /* WARNING: Could not recover jumptable at 0x00056a46. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*(code *)PTR_Diagnostic_UpdateActiveAggregate_00056ac4)();
  return;
}

