/* Ghidra analysis output; verify against original SH instructions. */

/* Headeru16 count/shift,word axes/values; calls10A48 and5B31C.3184 stock source-policy lookup cases
   cover duplicate axes/endpoints and shift0. Arbitrary table/shift validation not claimed. */

void Lookup_InterpolateWordCurve(undefined4 param_1,ushort *param_2)

{
  undefined4 uVar1;
  
  uVar1 = FUN_00010a48(param_1,(int)(short)*param_2,param_2 + 2,param_2 + *param_2 + 2,
                       param_2 + *param_2 + 2);
  (*(code *)PTR_FUN_000109c4)(uVar1);
  return;
}

