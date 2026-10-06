/* Ghidra analysis output; verify against original SH instructions. */

/* StockBAE40=1 forceszero;24910 stillcallswhenbypassfalse. Alternatecalibrations unmodeled. */

undefined4
Control_AdmitHighestPriorityOverride
          (float param_1,char param_2,ushort param_3,char param_4,char param_5,char param_6)

{
  char cVar1;
  undefined4 uVar2;
  
  if (((((*PTR_DAT_0002536c != '\0') || (param_2 != '\0')) ||
       (*(ushort *)PTR_DAT_00025370 <= param_3)) ||
      ((((param_1 < *(float *)PTR_DAT_00025374 || (*(float *)PTR_DAT_00025378 <= param_1)) &&
        (cVar1 = (*(code *)PTR_FUN_00025348)(PTR_DAT_0002537c), cVar1 != '\0')) ||
       ((param_4 != '\x01' || (param_5 != '\0')))))) || (param_6 != '\0')) {
    uVar2 = 0;
  }
  else {
    uVar2 = 1;
  }
  return uVar2;
}

