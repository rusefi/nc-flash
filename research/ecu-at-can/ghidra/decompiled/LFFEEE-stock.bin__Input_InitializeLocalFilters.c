/* Ghidra analysis output; verify against original SH instructions. */

/* Executed full initializer: GPIO words44A0/44A2, serial bank bytes44A4/44A5, threshold word44A6
   and previous samples; leaves44B0 unchanged. */

void Input_InitializeLocalFilters(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined1 uVar4;
  undefined2 uVar3;
  
  puVar1 = PTR_DAT_0000cb90;
  *(undefined2 *)PTR_DAT_0000cb90 = *(undefined2 *)(int)DAT_0000cb8c;
  *(undefined2 *)PTR_DAT_0000cb94 = *(undefined2 *)puVar1;
  puVar1 = PTR_DAT_0000cb98;
  *(undefined2 *)PTR_DAT_0000cb98 = *(undefined2 *)(int)DAT_0000cb8e;
  *(undefined2 *)PTR_DAT_0000cb9c = *(undefined2 *)puVar1;
  uVar4 = (*(code *)PTR_Input_ReadSerialBank_0000cba0)(1);
  *PTR_Input_FilteredSerialBankOne_0000cba4 = uVar4;
  *PTR_Input_PreviousSerialBankOne_0000cba8 = uVar4;
  uVar4 = (*(code *)PTR_Input_ReadSerialBank_0000cba0)(2);
  puVar1 = PTR_DAT_0000cbb0;
  *PTR_DAT_0000cbac = uVar4;
  puVar2 = PTR_Input_ReadThresholdBoolean_0000cbb4;
  *puVar1 = uVar4;
  uVar3 = (*(code *)puVar2)();
  puVar1 = PTR_DAT_0000cbbc;
  *(undefined2 *)PTR_DAT_0000cbb8 = uVar3;
  *(undefined2 *)puVar1 = uVar3;
  return;
}

