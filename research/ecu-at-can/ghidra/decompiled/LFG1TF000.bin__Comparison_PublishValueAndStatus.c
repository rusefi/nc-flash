/* Ghidra analysis output; verify against original SH instructions. */

/* A4D8=809C*10/256 forproducednonnegativeinput. A4DA=4 if92D5mask88, else1 if89B2==2, else2.
   Executed/modeledinside230F0. */

uint Comparison_PublishValueAndStatus(void)

{
  undefined2 uVar2;
  uint uVar1;
  
  uVar2 = (*(code *)PTR_FUN_00050b30)();
  *(undefined2 *)PTR_Comparison_PublishedValue_00050b28 = uVar2;
  uVar1 = (uint)(char)PTR_DAT_00050b34[1];
  if (((uVar1 & 8) == 0) &&
     (uVar1 = -((((int)(char)PTR_DAT_00050b34[1] & 0x80U) == 0) - 1), uVar1 == 0)) {
    if (*PTR_Comparison_SelectedCANStatus_00050b38 == '\x02') {
      *PTR_Comparison_PublishedStatus_00050b2c = 1;
      return 2;
    }
    *PTR_Comparison_PublishedStatus_00050b2c = 2;
    return 2;
  }
  *PTR_Comparison_PublishedStatus_00050b2c = 4;
  return uVar1;
}

