/* Ghidra analysis output; verify against original SH instructions. */

/* Unsigned6C92<40/>939 with914B exact1 produces8EF9/A.9462 exact1 clears8EFF; else inclusive40..939
   sets8EFF/8F00=1 regardless914B.16400 cases. See control-raw-enable.txt. */

char Control_QualifyRawChannel28(void)

{
  ushort uVar1;
  undefined *puVar2;
  undefined *puVar3;
  char cVar4;
  
  uVar1 = *(ushort *)PTR_DAT_0006ce80;
  cVar4 = *PTR_DAT_0006ce84;
  if ((uVar1 < *(ushort *)PTR_DAT_0006ce8c) && (cVar4 == '\x01')) {
    *PTR_DAT_0006ce88 = 1;
  }
  else {
    *PTR_DAT_0006ce88 = 0;
  }
  if ((*(ushort *)PTR_DAT_0006ce94 < uVar1) && (cVar4 == '\x01')) {
    *PTR_DAT_0006ce90 = 1;
  }
  else {
    *PTR_DAT_0006ce90 = 0;
  }
  puVar3 = PTR_FUN_0006cea0;
  puVar2 = PTR_DAT_0006ce9c;
  *PTR_DAT_0006ce98 = 0;
  cVar4 = (*(code *)puVar3)(puVar2);
  puVar2 = PTR_DAT_0006ce98;
  if (cVar4 == '\x01') {
    *PTR_DAT_0006cea4 = 0;
  }
  else if ((*(ushort *)PTR_DAT_0006ce8c <= uVar1) && (uVar1 <= *(ushort *)PTR_DAT_0006ce94)) {
    *PTR_DAT_0006cea4 = 1;
    *puVar2 = 1;
  }
  return cVar4;
}

