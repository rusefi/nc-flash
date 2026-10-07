/* Ghidra analysis output; verify against original SH instructions. */

/* Three seededwholeRAM normal-memorycases:0000..3FFFpreserved,4000..BF9Fcleared
   via100D8DMA;51C1=0;guardBFA0..BFA3retained. Originalbackup/stackrelocation/restore
   executes;nonvolatileGPR/GBR/SP preserved. No RAMfault/fullreset/physicalproof.
   control-initialize-syscr.txt. */

void Runtime_TestAndClearRam(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  char cVar4;
  undefined4 uVar5;
  undefined4 *puVar6;
  undefined4 *puVar7;
  
  puVar1 = PTR_PTR_000100b8;
  cVar4 = FUN_00010188(*(undefined4 *)PTR_PTR_000100b8,*(undefined4 *)PTR_PTR_000100bc);
  (*(code *)PTR_FUN_000100c0)();
  if (cVar4 == '\0') {
    (*(code *)PTR_FUN_000100c4)(*(int *)PTR_PTR_000100bc + 1);
    puVar3 = PTR_PTR_000100cc;
    puVar2 = PTR_PTR_000100c8;
    puVar7 = *(undefined4 **)puVar1;
    for (puVar6 = *(undefined4 **)PTR_PTR_000100c8; puVar6 < *(undefined4 **)puVar3;
        puVar6 = puVar6 + 1) {
      *puVar7 = *puVar6;
      puVar7 = puVar7 + 1;
    }
    FUN_00010188(*(undefined4 *)puVar2,*(undefined4 *)puVar3);
    (*(code *)PTR_FUN_000100c0)();
    puVar7 = *(undefined4 **)puVar1;
    for (puVar6 = *(undefined4 **)puVar2; puVar6 < *(undefined4 **)puVar3; puVar6 = puVar6 + 1) {
      uVar5 = *puVar7;
      puVar7 = puVar7 + 1;
      *puVar6 = uVar5;
    }
    (*(code *)PTR_FUN_000100d0)();
  }
  Runtime_ClearVolatileRamWithDma();
  *PTR_DAT_000100d4 = cVar4 != '\0';
  return;
}

