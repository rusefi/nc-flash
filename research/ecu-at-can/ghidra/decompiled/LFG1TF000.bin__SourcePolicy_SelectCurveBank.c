/* Ghidra analysis output; verify against original SH instructions. */

/* r4 lowbyte exactly1 decrements r5 byte before unsigned clamp0..4. Input0 decremented wraps255 and
   choosesbank4; exercised via all six wrappers. */

undefined4 SourcePolicy_SelectCurveBank(char param_1,char param_2)

{
  undefined4 uVar1;
  undefined1 local_8;
  
  local_8 = param_2;
  if (param_1 == '\x01') {
    local_8 = param_2 + -1;
  }
  uVar1 = (*(code *)PTR_FUN_00049b04)(local_8,0,4);
  return uVar1;
}

