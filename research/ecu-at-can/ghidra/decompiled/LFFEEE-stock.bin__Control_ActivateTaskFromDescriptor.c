/* Ghidra analysis output; verify against original SH instructions. */

/* Taskindex4 descriptor4110:availability11CB2->1,priority4112=1,391A selects4.192emptyqueue
   wholeRAM admissions atnonzeroSRmasks PASS. Inlinecontextswitch pathnotcovered. Word4queuefield
   istaskindexnotpriority. control-queued-event2.txt. */

undefined4 Control_ActivateTaskFromDescriptor(short param_1)

{
  char cVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  int iVar5;
  undefined4 uVar6;
  uint in_sr;
  
  puVar4 = PTR_FUN_00003694;
  puVar3 = PTR_DAT_00003690;
  puVar2 = PTR_DAT_0000368c;
  uVar6 = 0;
  cVar1 = *(char *)(*(int *)(PTR_DAT_00003690 + param_1 * 0x10 + 4) + 3);
  if (cVar1 == '\0') {
    uVar6 = 4;
    if (*(int *)PTR_DAT_000036a4 != 0) {
      (*(code *)PTR_FUN_000036a8)(4,1,*(undefined4 *)(PTR_DAT_0000368c + 8));
    }
  }
  else {
    *(char *)(*(int *)(PTR_DAT_00003690 + param_1 * 0x10 + 4) + 3) = cVar1 + -1;
    iVar5 = (*(code *)puVar4)(puVar2,(int)param_1,(int)(char)puVar3[param_1 * 0x10 + 2]);
    if (((iVar5 != 0) && (((int)DAT_00003686 & in_sr) == 0 && *(int *)(puVar2 + 8) == 0)) &&
       (*(char *)(*(int *)(puVar2 + 0x18) + 1) == '\0')) {
      *(int *)(puVar2 + 8) = (int)DAT_00003688;
      if (*(int *)PTR_DAT_00003698 != 0) {
        (*(code *)PTR_FUN_0000369c)(2);
      }
      (*(code *)PTR_FUN_000036a0)(puVar2);
    }
  }
  return uVar6;
}

