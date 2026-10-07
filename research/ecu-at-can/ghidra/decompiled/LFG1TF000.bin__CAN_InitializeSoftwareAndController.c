/* Ghidra analysis output; verify against original SH instructions. */

/* Executedinside11FA0/124F8:19AD0,1A056,1B060(0),1D4DA,1C912,1BB30,then1BBEA/1BBB0 establish8F6C0A.
   Fullcallercoverage,notindependentwholeRAMsemanticmodel. HCAN1AEAA component has256wholeRAM/MMIO
   cases. tcu-hcan-startup.txt. */

void CAN_InitializeSoftwareAndController(void)

{
  undefined *puVar1;
  undefined1 *puVar2;
  
  (*(code *)PTR_FUN_00019fc0)();
  FUN_0001a056();
  (*(code *)PTR_FUN_00019fc4)(0);
  (*(code *)PTR_FUN_00019fc8)();
  (*(code *)PTR_FUN_00019fcc)();
  (*(code *)PTR_FUN_00019fd0)();
  puVar2 = (undefined1 *)(int)DAT_00019fb8;
  *(undefined1 *)(int)DAT_00019fb6 = 0;
  puVar1 = PTR_FUN_00019fd4;
  *puVar2 = 0;
  (*(code *)puVar1)();
  (*(code *)PTR_FUN_00019fd8)();
  return;
}

