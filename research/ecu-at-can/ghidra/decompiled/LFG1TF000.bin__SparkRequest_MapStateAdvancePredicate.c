/* Ghidra analysis output; verify against original SH instructions. */

/* Calls4D350 then4D7A2: signed80EE>=ref-64*selectedbyte. Verified in complete lifecycle. See
   tcu-request-dispatch.txt. */

undefined4 SparkRequest_MapStateAdvancePredicate(undefined4 param_1,undefined4 param_2)

{
  undefined4 uVar1;
  
  uVar1 = (*(code *)PTR_SparkRequest_SelectAdvanceMargin_0004cfe8)(param_2);
  uVar1 = (*(code *)PTR_SparkRequest_CompareAdvanceMargin_0004cfec)(uVar1,param_2);
  return uVar1;
}

