/* Ghidra analysis output; verify against original SH instructions. */

/* Executed: clearsA520/A521; see tcu-pulse-input.txt. */

void PulseInput_InitializePublication(void)

{
  undefined *puVar1;
  
  puVar1 = PTR_PulseInput_PublicationStatus_00051390;
  *PTR_PulseInput_PublishedByte_0005138c = 0;
  *puVar1 = 0;
  return;
}

