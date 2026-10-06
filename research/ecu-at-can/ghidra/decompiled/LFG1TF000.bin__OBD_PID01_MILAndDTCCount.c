/* Ghidra analysis output; verify against original SH instructions. */

/* Outputs01,(stored DTC count plus80 ifA99B nonzero),04,00,00. Executed healthy00 and
   storedU0100/MIL81; no ISO-TP transport simulation. */

undefined4 OBD_PID01_MILAndDTCCount(int param_1)

{
  undefined *puVar1;
  undefined *puVar2;
  char cVar3;
  
  cVar3 = (*(code *)PTR_FUN_0005439c)(*(int *)(param_1 + 4) + 1);
  puVar1 = PTR_DAT_000543a4;
  if (*(char *)(int)DAT_00054396 != '\0') {
    cVar3 = cVar3 + (char)DAT_00054398;
  }
  **(undefined1 **)(param_1 + 4) = 1;
  *(char *)(*(int *)(param_1 + 4) + 1) = cVar3;
  *(undefined *)(*(int *)(param_1 + 4) + 2) = *PTR_DAT_000543a0;
  puVar2 = PTR_DAT_000543a8;
  *(undefined *)(*(int *)(param_1 + 4) + 3) = *puVar1;
  *(undefined *)(*(int *)(param_1 + 4) + 4) = *puVar2;
  return 5;
}

