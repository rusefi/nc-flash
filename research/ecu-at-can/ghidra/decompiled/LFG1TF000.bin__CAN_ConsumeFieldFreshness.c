/* Ghidra analysis output; verify against original SH instructions. */

/* Atomic read-and-clear from8F82 using offset5C9A0 and mask5C9CF indexed by field number. */

int CAN_ConsumeFieldFreshness(byte param_1)

{
  byte bVar1;
  byte bVar2;
  
  (*(code *)PTR_FUN_0001c07c)();
  bVar1 = PTR_DAT_0001c088[(byte)PTR_DAT_0001c084[param_1]];
  bVar2 = PTR_DAT_0001c08c[param_1];
  if ((bVar1 & bVar2) != 0) {
    PTR_DAT_0001c088[(byte)PTR_DAT_0001c084[param_1]] =
         PTR_DAT_0001c088[(byte)PTR_DAT_0001c084[param_1]] & ~PTR_DAT_0001c08c[param_1];
  }
  (*(code *)PTR_FUN_0001c080)();
  return (int)(char)(bVar1 & bVar2);
}

