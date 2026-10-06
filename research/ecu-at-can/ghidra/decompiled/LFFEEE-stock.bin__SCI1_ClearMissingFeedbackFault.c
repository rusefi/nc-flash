/* Ghidra analysis output; verify against original SH instructions. */

/* Original explicit clear writes protected20A8=00FF. Executed then251 enabledmonitorcalls
   set57CD;caller/admission andphysicalrecovery remainopen. */

void SCI1_ClearMissingFeedbackFault(void)

{
  (*(code *)PTR_FUN_0002863c)(PTR_SCI1_MissingFeedbackFault_00028638,0);
  return;
}

