/* Ghidra analysis output; verify against original SH instructions. */

/* Protected6818 from6800 times selected gain, clamp -125 to selected upper. Raw gate branches
   independently checked; stock gain12.5. */

void Control_ProduceScaledErrorTerm(void)

{
  undefined4 uVar1;
  float fVar2;
  
  if (((*PTR_DAT_000316cc == '\0') || (*PTR_DAT_000316d0 == '\x01')) ||
     (*PTR_DAT_000316d4 == '\x01')) {
    fVar2 = *(float *)PTR_Control_BoundedInputError_000316c8 * *(float *)PTR_DAT_000316d8;
    uVar1 = DAT_000316e4;
    if (*PTR_ControlInput_UpperLimitGate_000316dc == '\x01') {
      uVar1 = *(undefined4 *)PTR_DAT_000316e0;
    }
  }
  else {
    fVar2 = *(float *)PTR_Control_BoundedInputError_000316c8 * *(float *)PTR_DAT_000316e8;
    uVar1 = *(undefined4 *)PTR_DAT_000316ec;
  }
  uVar1 = (*(code *)PTR_FUN_000316f4)(fVar2,DAT_000316f0,uVar1);
  (*(code *)PTR_FUN_000316fc)(uVar1,PTR_Control_ScaledErrorTerm_000316f8);
  return;
}

