/* Ghidra analysis output; verify against original SH instructions. */

/* Executed512 wordcases:44A2bit0->722A byte+complement via154C0.Retainedtasks observeactualwriter
   at154CA. PFDRbit0 provenance viaoriginalCA94; physicalpinroleunproved. control-task-stop.txt. */

void Control_PublishFilteredModeInput(void)

{
  (*(code *)PTR_FUN_00041140)
            (PTR_Control_FilteredModeInput_0004113c,(*(ushort *)PTR_DAT_00041138 & 1) != 0);
  return;
}

