/* Ghidra analysis output; verify against original SH instructions. */

/* Executed raw bytes0-1 ->89DC/DD;89DE=1 forFFFF,2 otherwise. */

void CAN201_CopyWord0AndValidity(void)

{
  undefined *puVar1;
  uint uVar2;
  undefined1 uVar3;
  
  uVar2 = (*(code *)PTR_CAN201_GetWord0_00018190)();
  puVar1 = PTR_DAT_00018188;
  *PTR_DAT_00018184 = (char)((uVar2 & 0xffff) >> 8);
  *puVar1 = (char)(uVar2 & 0xffff);
  uVar3 = 2;
  if ((undefined *)(uVar2 & 0xffff) == PTR_DAT_00018194) {
    uVar3 = 1;
  }
  *PTR_DAT_0001818c = uVar3;
  return;
}

