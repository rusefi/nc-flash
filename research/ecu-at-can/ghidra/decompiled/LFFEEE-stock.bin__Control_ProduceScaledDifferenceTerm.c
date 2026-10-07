/* Ghidra analysis output; verify against original SH instructions. */

/* 6824 from6804 times selected gain, clamped. Stock gains zero; finite stock cases only. Physical
   loop identity open. */

void Control_ProduceScaledDifferenceTerm(void)

{
  undefined4 uVar1;
  float fVar2;
  
  if (((*PTR_DAT_000316cc == '\0') || (*PTR_DAT_000316d0 == '\x01')) ||
     (*PTR_DAT_000316d4 == '\x01')) {
    fVar2 = *(float *)PTR_Control_BoundedErrorDifference_00031714 * *(float *)PTR_DAT_00031718;
    uVar1 = DAT_000316e4;
    if (*PTR_ControlInput_UpperLimitGate_000316dc == '\x01') {
      uVar1 = *(undefined4 *)PTR_DAT_0003171c;
    }
  }
  else {
    fVar2 = *(float *)PTR_Control_BoundedErrorDifference_00031714 * *(float *)PTR_DAT_00031720;
    uVar1 = *(undefined4 *)PTR_DAT_00031724;
  }
  uVar1 = (*(code *)PTR_FUN_000316f4)(fVar2,DAT_000316f0,uVar1);
  *(undefined4 *)PTR_Control_ScaledDifferenceTerm_00031728 = uVar1;
  return;
}

