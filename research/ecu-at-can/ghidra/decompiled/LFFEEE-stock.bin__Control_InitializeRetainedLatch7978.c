/* Ghidra analysis output; verify against original SH instructions. */

/* Copies protected722E into7984 and clears protected7978; physical control role unresolved. */

void Control_InitializeRetainedLatch7978(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined1 uVar3;
  
  uVar3 = (*(code *)PTR_FUN_0004e9f8)(PTR_DAT_0004e9f4);
  puVar2 = PTR_FUN_0004ea04;
  puVar1 = PTR_Control_RetainedLatch7978_0004ea00;
  *PTR_DAT_0004e9fc = uVar3;
  (*(code *)puVar2)(puVar1,0);
  return;
}

