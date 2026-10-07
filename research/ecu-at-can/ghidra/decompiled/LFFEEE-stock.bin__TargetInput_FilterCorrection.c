/* Ghidra analysis output; verify against original SH instructions. */

/* Original2508 filters695C towardold67E0 withDB148~.9951 retention, eps.0048828125;207C
   clamps7..16. Runsinside30CE4 onlywhen8F30zero. */

void TargetInput_FilterCorrection(void)

{
  undefined4 uVar1;
  
  uVar1 = (*(code *)PTR_FUN_00033cb0)
                    (*(undefined4 *)PTR_TargetInput_MappedCorrection_00033cac,
                     *(undefined4 *)PTR_TargetInput_RetainedCorrection_00033ca8,
                     1.0 - *(float *)PTR_DAT_00033ca0,DAT_00033ca4);
  uVar1 = (*(code *)PTR_FUN_00033cbc)
                    (uVar1,*(undefined4 *)PTR_DAT_00033cb8,*(undefined4 *)PTR_DAT_00033cb4);
  *(undefined4 *)PTR_TargetInput_RetainedCorrection_00033ca8 = uVar1;
  return;
}

