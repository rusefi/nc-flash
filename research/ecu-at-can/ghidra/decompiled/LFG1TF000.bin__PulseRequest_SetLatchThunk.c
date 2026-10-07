/* Ghidra analysis output; verify against original SH instructions. */

/* Executed tailcall23DC0 sets9418=1;repeatrequestscoalesce beforeproducerconsumes. */

void PulseRequest_SetLatchThunk(void)

{
                    /* WARNING: Could not recover jumptable at 0x000535b6. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*(code *)PTR_ModePulse_RequestSecond_000535dc)();
  return;
}

