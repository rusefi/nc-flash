/* Ghidra analysis output; verify against original SH instructions. */

/* Executed:90A7=indexXOR1 undercriticalsection,clear90B7bit7;oldrecord90AC+2indexbit1 chooses1D85E
   build else1D9F2 cleanup. Indices0/1 tested; wiretransmissionunproved. */

void Diagnostic_HandoffResponseRecord(uint param_1,short param_2)

{
  undefined *puVar1;
  
  (*(code *)PTR_FUN_0001da88)();
  puVar1 = PTR_FUN_0001da8c;
  *PTR_Diagnostic_CurrentRecordIndex_0001da90 = (byte)param_1 ^ 1;
  (*(code *)puVar1)();
  *PTR_DAT_0001da94 = *PTR_DAT_0001da94 & 0x7f;
  if ((PTR_Diagnostic_ResponseRecordFlags_0001da98[(param_1 & 0xff) * 2] & 2) != 0) {
    Diagnostic_ConstructResponseBuffer(param_1,(int)param_2);
    return;
  }
  Diagnostic_CleanupResponseRecord(param_1,0);
  return;
}

