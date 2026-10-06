/* Ghidra analysis output; verify against original SH instructions. */

/* Byte count/axis/value table ->10922, scaling256. All65536 inputs of stock703C0 verified through
   original software arithmetic; see software-lookup.txt. */

void Lookup_ByteCurveToFixedPoint(undefined4 param_1,byte *param_2)

{
  Lookup_InterpolateByteCurve
            (param_1,(int)(char)*param_2,param_2 + 1,param_2 + *param_2 + 1,param_2 + 1,
             param_2 + *param_2 + 1);
  return;
}

