/* Ghidra analysis output; verify against original SH instructions. */

/* Initializes six raw/working words to10000. */

void CAN4B0_InitializeWords(void)

{
  undefined2 uVar1;
  undefined *puVar2;
  
  puVar2 = PTR_CAN4B0_WorkingWord6_0003600c;
  uVar1 = DAT_00035ff4;
  *(undefined2 *)PTR_CAN4B0_WorkingWord4_00036008 = DAT_00035ff4;
  *(undefined2 *)puVar2 = uVar1;
  puVar2 = PTR_DAT_00036028;
  *(undefined2 *)PTR_DAT_00036024 = uVar1;
  *(undefined2 *)puVar2 = uVar1;
  puVar2 = PTR_DAT_00036018;
  *(undefined2 *)PTR_DAT_00036014 = uVar1;
  *(undefined2 *)puVar2 = uVar1;
  return;
}

