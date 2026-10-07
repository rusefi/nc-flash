/* Ghidra analysis output; verify against original SH instructions. */

/* Add selected/clamped scaled6800 increment to6820; clamp0..6814. Stock gain .78125; limit producer
   remains open. */

void Control_AccumulateScaledErrorTerm(void)

{
  undefined4 uVar1;
  float fVar2;
  
  if (((*PTR_DAT_000316cc == '\0') || (*PTR_DAT_000316d0 == '\x01')) ||
     (*PTR_DAT_000316d4 == '\x01')) {
    fVar2 = *(float *)PTR_Control_BoundedInputError_000316c8 * *(float *)PTR_DAT_00031700;
    uVar1 = DAT_000316e4;
    if (*PTR_ControlInput_UpperLimitGate_000316dc == '\x01') {
      uVar1 = *(undefined4 *)PTR_DAT_00031704;
    }
  }
  else {
    fVar2 = *(float *)PTR_Control_BoundedInputError_000316c8 * *(float *)PTR_DAT_00031708;
    uVar1 = *(undefined4 *)PTR_DAT_0003170c;
  }
  fVar2 = (float)(*(code *)PTR_FUN_000316f4)(fVar2,DAT_000316f0,uVar1);
  uVar1 = (*(code *)PTR_FUN_000316f4)
                    (*(float *)PTR_Control_AccumulatedErrorTerm_00031710 + fVar2,0,
                     *(undefined4 *)PTR_Control_AccumulatedErrorLimit_000316a8);
  *(undefined4 *)PTR_Control_AccumulatedErrorTerm_00031710 = uVar1;
  return;
}

