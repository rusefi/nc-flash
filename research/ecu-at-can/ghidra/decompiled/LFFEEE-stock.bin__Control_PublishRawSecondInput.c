/* Ghidra analysis output; verify against original SH instructions. */

/* 8F30 any nonzero selects ROM B8158=20 else40E0 into protected6D40.7016 zero copies to raw6D48
   else retains.9216 cases/all flag bytes and320 retained cycles; source/sensor identity open. */

uint Control_PublishRawSecondInput(void)

{
  uint uVar1;
  undefined4 extraout_fr0;
  
  if (*PTR_Control_RawSecondFallbackLatch_00039f90 == '\0') {
    (*(code *)PTR_FUN_00039f9c)
              (*(undefined4 *)PTR_DAT_00039f94,PTR_Control_RawSecondPublished_00039f98);
  }
  else {
    (*(code *)PTR_FUN_00039f9c)
              (*(undefined4 *)PTR_DAT_00039fa0,PTR_Control_RawSecondPublished_00039f98);
  }
  uVar1 = (*(code *)PTR_FUN_00039fa8)(PTR_DAT_00039fa4);
  uVar1 = uVar1 & 0xff;
  if (uVar1 == 0) {
    uVar1 = (*(code *)PTR_FUN_00039fac)(PTR_Control_RawSecondPublished_00039f98);
    *(undefined4 *)PTR_Control_RawSecondSnapshot_00039fb0 = extraout_fr0;
  }
  return uVar1;
}

