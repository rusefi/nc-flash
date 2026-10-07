/* Ghidra analysis output; verify against original SH instructions. */

/* Original2508 filters683C into6840; stockretention~.84, finiteRTZ/nofusedFMAC,
   near-targetsnap.36directcases plus320retainedcycles. */

void ControlSecondary_FilterTarget(void)

{
  undefined4 uVar1;
  
  uVar1 = (*(code *)PTR_FUN_00031a34)
                    (*(undefined4 *)PTR_ControlSecondary_Target_00031a00,
                     *(undefined4 *)PTR_ControlSecondary_FilteredTarget_00031a30,
                     1.0 - *(float *)PTR_DAT_00031a28,DAT_00031a2c);
  *(undefined4 *)PTR_ControlSecondary_FilteredTarget_00031a30 = uVar1;
  return;
}

