/* Ghidra analysis output; verify against original SH instructions. */

/* Executed asymmetriccleanup:optionalstatusbit2,1D83A
   timer,clear90A8bit4;record0zeroC2/C4,clear90ACbits3/4/5,90B7bit6,8F90bits6/7;record1criticalclear90AEbit5.
   Buffers/lengthsretain. */

uint Diagnostic_CleanupResponseRecord(byte param_1,char param_2)

{
  char cVar1;
  undefined *puVar2;
  undefined *puVar3;
  uint uVar4;
  
  puVar2 = PTR_DAT_0001da80;
  if ((PTR_Diagnostic_FirstErrorBytes_0001daa0[param_1] == '\0') && (param_2 == '\0')) {
    PTR_DAT_0001da80[(uint)param_1 * 2 + 1] = PTR_DAT_0001da80[(uint)param_1 * 2 + 1] | 4;
  }
  Diagnostic_ConditionallyReloadTimer();
  *PTR_DAT_0001daa4 = *PTR_DAT_0001daa4 & 0xef;
  puVar3 = PTR_DAT_0001daac;
  if (param_1 == 0) {
    *(undefined2 *)PTR_DAT_0001daa8 = 0;
    *(undefined2 *)puVar3 = 0;
    puVar2[1] = puVar2[1] & 0xe7;
    puVar3 = PTR_DAT_0001da9c;
    *PTR_DAT_0001da94 = *PTR_DAT_0001da94 & 0xbf;
    *puVar3 = *puVar3 & 0x3f;
    cVar1 = puVar2[1];
    puVar2[1] = (char)((int)cVar1 & 0xdfU);
    return (int)cVar1 & 0xdfU;
  }
  (*(code *)PTR_FUN_0001da88)();
  puVar2[3] = puVar2[3] & 0xdf;
  uVar4 = (*(code *)PTR_FUN_0001da8c)();
  return uVar4;
}

