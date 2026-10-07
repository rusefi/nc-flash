/* Ghidra analysis output; verify against original SH instructions. */

/* Whole-application-RAM independent model1280 cases and16 actualtaskreturns PASS.
   Reset9415==1/oldA954==0 clears3 gates/states; originalphase0/4 calls. See
   tcu-qualified-receive.txt. */

void Diagnostic_UpdateAdmissionGates(void)

{
  char cVar1;
  undefined1 auStack_14 [4];
  undefined1 auStack_10 [4];
  undefined1 auStack_c [8];
  
  cVar1 = (*(code *)PTR_FUN_00056b74)();
  if ((cVar1 == '\x01') && (*(char *)(int)DAT_00056b5a == '\0')) {
    FUN_00056ae8();
  }
  *(char *)(int)DAT_00056b5a = cVar1;
  Diagnostic_ComputeAdmissionConditions(auStack_c,auStack_10,auStack_14);
  Diagnostic_UpdateAdmissionDeadline(PTR_DAT_00056b68,auStack_c,PTR_DAT_00056b5c);
  Diagnostic_UpdateAdmissionDeadline
            (PTR_DAT_00056b6c,auStack_10,PTR_Diagnostic_CommunicationAdmission_00056b60);
  Diagnostic_UpdateAdmissionDeadline(PTR_DAT_00056b70,auStack_14,PTR_DAT_00056b64);
  return;
}

