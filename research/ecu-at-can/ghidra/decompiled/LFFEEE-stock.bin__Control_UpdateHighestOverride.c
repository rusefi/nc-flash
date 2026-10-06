/* Ghidra analysis output; verify against original SH instructions. */

/* 566C exact1 writesmax(BB170=1,BB174~0.2), elsezero to protected565C. Stock24910 never admits this
   branch; direct enable fixtures tested. */

void Control_UpdateHighestOverride(void)

{
  char cVar1;
  undefined4 uVar2;
  
  cVar1 = (*(code *)PTR_FUN_00024720)(PTR_DAT_0002471c);
  if (cVar1 == '\x01') {
    uVar2 = (*(code *)PTR_FUN_0002472c)
                      (*(undefined4 *)PTR_DAT_00024728,*(undefined4 *)PTR_DAT_00024724);
  }
  else {
    uVar2 = 0;
  }
  (*(code *)PTR_FUN_00024718)(uVar2,PTR_Control_HighestOverrideValue_00024714);
  return;
}

