/* Ghidra analysis output; verify against original SH instructions. */

/* Tailcall2094E; full128B6 caller executed across256 modes and3 count boundaries. See
   tcu-reference-policy.txt. */

void Reference_ServiceElapsedCaptureCounter(void)

{
  (*DAT_0001e5e8)();
  return;
}

