/* Ghidra analysis output; verify against original SH instructions. */

/* Calls171CC,17070,18158.1225 tested callbacks read only payload0/1/6; not a global non-use proof
   for4/5. */

void CAN201_ApplicationCallback(void)

{
  (*(code *)PTR_CAN201_ConvertWord0_0001ad80)();
  (*(code *)PTR_CAN201_ConvertByte6_0001ad84)();
                    /* WARNING: Could not recover jumptable at 0x0001ace8. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*(code *)PTR_CAN201_CopyWord0AndValidity_0001ad88)();
  return;
}

