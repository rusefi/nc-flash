/* Ghidra analysis output; verify against original SH instructions. */

/* Table5E1E8 indexedold8081 andrequestedr4; stock6x6 stepsone towardrequest.916Cbit0 bypasses.
   Priortransitionr5==0B speciallowrequestcase.144 complete48C08 fixtures exerciseordinarypath. */

uint Selection_SelectOneStepCandidate(uint param_1,char param_2)

{
  uint uVar1;
  
  uVar1 = param_1;
  if ((((*PTR_DAT_00047bac & 1) != 1) &&
      (uVar1 = (int)(char)PTR_Selection_OneStepTable_00047bb0
                          [(param_1 & 0xff) + (uint)CAN231_SixStateSource * 6], param_2 == '\v')) &&
     ((param_1 & 0xff) < 2)) {
    uVar1 = 1;
  }
  return uVar1;
}

