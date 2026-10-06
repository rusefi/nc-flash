/* Ghidra analysis output; verify against original SH instructions. */

/* StockBAE43=1 disablesmode1 branch;568B1,722A0,92CB/932Aqualifier andtimer625/2136/566A
   conditions. Full24910 oracle;control-admission.txt. */

undefined4
Control_AdmitRelativeOverride
          (char param_1,ushort param_2,ushort param_3,char param_4,char param_5,char param_6,
          char param_7,char param_8)

{
  ushort uVar1;
  char cVar2;
  undefined4 uVar3;
  
  uVar1 = (*(code *)PTR_FUN_00025584)
                    ((int)*(short *)PTR_DAT_00025578,(int)*(short *)PTR_DAT_00025580);
  if ((param_6 == '\x01') &&
     (((((*PTR_DAT_00025588 == '\0' && (param_1 == '\x01')) &&
        (cVar2 = (*(code *)PTR_Protected_ReadByteOrDefault_00025554)(PTR_DAT_0002558c,0),
        cVar2 == '\0')) &&
       ((*(ushort *)PTR_Control_RelativeOverrideTimer_00025590 < *(ushort *)PTR_DAT_00025580 &&
        ((param_5 == '\x01' || ((*(ushort *)PTR_DAT_00025578 <= param_3 && (param_3 <= uVar1))))))))
      || ((param_1 == '\0' &&
          ((((*PTR_DAT_00025594 == '\0' && (*PTR_DAT_00025598 == '\0')) || (param_8 == '\x01')) &&
           (((param_4 == '\x01' && (param_7 == '\x01')) || (*(ushort *)PTR_DAT_00025578 <= param_2))
           )))))))) {
    uVar3 = 1;
  }
  else {
    uVar3 = 0;
  }
  return uVar3;
}

