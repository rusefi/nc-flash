/* Ghidra analysis output; verify against original SH instructions. */

/* Executed criticalsection1B9F6/1BA24 aroundclearbit1
   at90AC+2*argumentlowbyte;nestcount/SRrestored,savedmask8F65 refreshedwhenoutermost. */

void Diagnostic_ClearResponsePending(byte param_1)

{
  (*(code *)PTR_FUN_0001d32c)();
  PTR_Diagnostic_ResponseRecordFlags_0001d320[(uint)param_1 * 2] =
       PTR_Diagnostic_ResponseRecordFlags_0001d320[(uint)param_1 * 2] & 0xfd;
  (*(code *)PTR_FUN_0001d330)();
  return;
}

