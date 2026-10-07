/* Ghidra analysis output; verify against original SH instructions. */

/* Originalsoftwareconversion ofdouble+0.5 returnsinteger0; doesnotroundtheargument.
   Executednested3AC70. */

int ClassBase_ConstantZero(void)

{
  short sVar1;
  
  sVar1 = (*(code *)PTR_FUN_0003af24)();
  return (int)sVar1;
}

