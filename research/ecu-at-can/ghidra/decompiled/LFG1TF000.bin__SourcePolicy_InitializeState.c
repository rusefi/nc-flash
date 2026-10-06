/* Ghidra analysis output; verify against original SH instructions. */

/* Zero9C90/91/92/93/94 and word9C96. Original source-policy initialization;
   tcu-source-selection.txt. */

void SourcePolicy_InitializeState(void)

{
  undefined *puVar1;
  undefined2 *puVar2;
  undefined1 *puVar3;
  
  puVar1 = PTR_SourcePolicy_RejectedDecrement_000496d4;
  *(undefined1 *)(int)DAT_000496ca = 0;
  *puVar1 = 0;
  puVar3 = (undefined1 *)(int)DAT_000496ce;
  *(undefined1 *)(int)DAT_000496cc = 0;
  *puVar3 = 0;
  puVar2 = (undefined2 *)(int)DAT_000496d0;
  *PTR_SourcePolicy_AdjustmentState_000496d8 = 0;
  *puVar2 = 0;
  return;
}

