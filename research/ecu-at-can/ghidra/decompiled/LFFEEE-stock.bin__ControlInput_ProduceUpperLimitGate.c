/* Ghidra analysis output; verify against original SH instructions. */

/* 6939 requires67D0>=10 and6929zero. Permission(7346exact1 and65D0zero) ORstockDB0B8=1; stock
   bypasses first check.320rawflag/boundarycases. */

undefined4 ControlInput_ProduceUpperLimitGate(void)

{
  char cVar1;
  
  cVar1 = (*(code *)PTR_FUN_000309e8)(PTR_DAT_000309e4);
  if ((((cVar1 != '\x01') || (*PTR_DAT_000309ec != '\0')) && (*PTR_DAT_000309f0 == '\0')) ||
     ((*(float *)PTR_ControlMode_BiasedInput_000309f8 < *(float *)PTR_DAT_000309f4 ||
      (*PTR_DAT_000309fc != '\0')))) {
    *DAT_00030a00 = 0;
  }
  else {
    *DAT_00030a00 = 1;
  }
  return 0;
}

