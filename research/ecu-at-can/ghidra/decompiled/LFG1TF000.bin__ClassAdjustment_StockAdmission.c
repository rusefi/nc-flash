/* Ghidra analysis output; verify against original SH instructions. */

/* Stock signed80F2 must be >=77142=12800 AND <77144=12800: impossible. Exhaustive65536 original
   calls return0 and clear821E. Getters execute; see tcu-class-admission.txt. */

undefined4 ClassAdjustment_StockAdmission(void)

{
  short sVar1;
  short sVar2;
  short sVar3;
  char cVar4;
  char cVar5;
  undefined4 uVar6;
  
  sVar3 = DAT_ffff80f2;
  sVar1 = *(short *)PTR_DAT_00036c98;
  sVar2 = *(short *)PTR_DAT_00036c9c;
  cVar4 = (*(code *)PTR_FUN_00036ca0)();
  cVar5 = (*(code *)PTR_FUN_00036ca4)();
  if (((((cVar5 == '\0') || ((*PTR_DAT_00036ca8 & 1) != 0)) || (cVar4 == '\x05')) ||
      (((cVar4 == '\0' || (sVar1 < *(short *)PTR_DAT_00036cac)) ||
       ((*(short *)PTR_DAT_00036cb0 <= sVar1 ||
        ((sVar3 < *(short *)PTR_DAT_00036cb4 || (*(short *)PTR_DAT_00036cb8 <= sVar3)))))))) ||
     ((sVar2 < *(short *)PTR_DAT_00036cbc ||
      ((((*(short *)PTR_DAT_00036cc0 <= sVar2 || ((*PTR_DAT_00036cc4 & 4) != 0)) ||
        ((*PTR_DAT_00036cc8 & 4) == 0)) || (*(short *)PTR_DAT_00036ccc < *(short *)PTR_DAT_00036cd0)
       ))))) {
    uVar6 = 0;
    *PTR_DAT_00036cd4 = 0;
  }
  else {
    uVar6 = 1;
  }
  return uVar6;
}

