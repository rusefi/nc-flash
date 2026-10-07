/* Ghidra analysis output; verify against original SH instructions. */

/* 128wholeapplicationRAMcases toDCF8 PASS:mode0
   queues0/17,selects17priority4,context12BC=FFFF11A8/maskB0. OriginalRTEtoDCF8/SR0/nativeSP. No
   fullreset/hardwaretiming. control-scheduler-start.txt. */

void Scheduler_InitializeStockMode(undefined1 param_1)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  
  puVar2 = PTR_PTR_00003e50;
  puVar1 = PTR_DAT_00003e48;
  *(undefined4 *)(PTR_DAT_00003e48 + 0x10) = *(undefined4 *)PTR_DAT_00003e4c;
  puVar1[1] = param_1;
  *(undefined4 *)(puVar1 + 0xc) = *(undefined4 *)puVar2;
  *(undefined2 *)(puVar1 + 4) = 0xffff;
  puVar2 = PTR_DAT_00003e54;
  *(undefined **)(puVar1 + 0x18) = PTR_DAT_00003e54;
  puVar3 = PTR_FUN_00003e58;
  *(undefined4 *)(puVar1 + 0x14) = *(undefined4 *)(puVar2 + 4);
  (*(code *)puVar3)(puVar1);
  (*(code *)PTR_Control_InitializeTaskAvailability_00003e5c)(puVar1);
  (*(code *)PTR_FUN_00003e60)(puVar1);
  (*(code *)PTR_FUN_00003e64)(puVar1);
  (*(code *)PTR_FUN_00003e68)();
  (*(code *)PTR_FUN_00003e6c)();
  (*(code *)PTR_FUN_00003e70)(puVar1);
  (*(code *)PTR_FUN_00003e74)(puVar1);
  if (*(int *)PTR_DAT_00003e78 != 0) {
    (*(code *)PTR_FUN_00003e7c)();
  }
  (*(code *)PTR_FUN_00003e80)();
  (*(code *)PTR_FUN_00003e84)(puVar1);
  return;
}

